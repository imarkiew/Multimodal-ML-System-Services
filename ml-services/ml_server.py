from flask import Flask, request, jsonify
import base64
import requests
import json
import sqlalchemy as db
import csv
from sqlalchemy.orm import sessionmaker
from argparse import ArgumentParser
from examinations import Examinations


parser = ArgumentParser()
parser.add_argument("--service_address", help="Service IP address", type=str, required=True)
parser.add_argument("--service_port", help="Service port", type=str, required=True)
parser.add_argument("--db_url", help="MySQL database url", type=str, required=True)
parser.add_argument("--ml_model_url", help="ML model url", type=str, required=True)
parser.add_argument("--output_dir", help="Output directory for saving files", type=str, required=True)
parser.add_argument("--label_class_matcher_file_path_for_skin_lesions", help="Label - class matcher file path for skin lesions", type=str, required=True)
args = parser.parse_args()
arguments = args.__dict__

app = Flask(__name__)

engine = db.create_engine(arguments["db_url"])
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/skinLesions", methods=["POST"])
def handle_skin_lesions_request():
    try:
        body = request.json

        # discard metainfo from base64 encoded image
        content = body["content"].split(",")[1]
        path = arguments["output_dir"] + body["fileName"]

        with open(path, "wb") as f:
            f.write(base64.b64decode(content))

        data = json.dumps({"signature_name": "serving_default", "instances": [{"b64": content}]})
        headers = {"content-type": "application/json"}
        json_response = requests.post(arguments["ml_model_url"], data=data, headers=headers)
        predictions = json.loads(json_response.text)

        predictions = parse_json_with_predictions_for_skin_lesions(predictions, arguments["label_class_matcher_file_path_for_skin_lesions"], to_percent_and_round)

        print(predictions)

        session.add(Examinations(kind="skin-lesions", title=body["title"], date=body["date"],
                                results=predictions, path=path, username=body["username"]))
        session.commit()

        response = jsonify(success=True)
        response.status_code = 200
        return response
    except:
        response = jsonify(success=False)
        response.status_code = 500
        return response


def parse_json_with_predictions_for_skin_lesions(predictions, label_class_matcher_file_path, customize_printed_value):
    predictions = predictions["predictions"][0]
    with open(label_class_matcher_file_path, "r") as file:
        label_class_matcher = csv.DictReader(file, delimiter=",")
        return json.dumps({match["class"]: customize_printed_value(predictions[int(match["label"])]) for match in label_class_matcher})


def to_percent_and_round(value, digits=2):
    return round(100 * value, digits)


if __name__ == "__main__":
    app.run(host=arguments["service_address"], port=arguments["service_port"])
