"""
.. module:: server
   :synopsis: Proxy server between ML models, database and play server
"""


from flask import Flask, request, jsonify
import json
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from argparse import ArgumentParser
from examinations import Examinations
from utilities import parse_predictions_for_skin_lesions, to_percent_and_round, \
    preprocess_content_from_request_body, read_breast_cancer_file, get_response_fom_ml_service, parse_predictions_for_breast_cancer


parser = ArgumentParser()
parser.add_argument("--config_file_path", help="Config file path", type=str, required=True)
parser.add_argument("--config_type", help="Config type", type=str, required=True)
args = parser.parse_args()
arguments = args.__dict__

with open(arguments["config_file_path"], "r") as file:
    config_file = json.load(file)[arguments["config_type"]]

app = Flask(__name__)

engine = db.create_engine(config_file["db_url"])
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/skinLesions", methods=["POST"])
def handle_skin_lesions_request():
    """Handle incoming HTTP POST request with json body for skin lesions

       Returns:
          HTTP response with 200 status if there wasn't any exception and 500 otherwise
   """
    try:
        body = request.json
        content, path = preprocess_content_from_request_body(body, config_file["skin_lesions_output_dir"])
        data = json.dumps({"signature_name": "serving_default", "instances": [{"b64": content}]})
        json_response = get_response_fom_ml_service(data, config_file["skin_lesions_ml_model_url"])
        predictions = parse_predictions_for_skin_lesions(json_response.text, config_file["skin_lesions_labels_classes_matcher"], to_percent_and_round)

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


@app.route("/breastCancer", methods=["POST"])
def handle_breast_cancer_request():
    """Handle incoming HTTP POST request with json body for breast cancer

       Returns:
           HTTP response with 200 status if there wasn't any exception and 500 otherwise
    """
    try:
        body = request.json
        _, path = preprocess_content_from_request_body(body, config_file["breast_cancer_output_dir"])
        data = read_breast_cancer_file(path)
        json_response = get_response_fom_ml_service(data, config_file["breast_cancer_ml_model_url"])
        predictions = parse_predictions_for_breast_cancer(json_response.text, to_percent_and_round)

        session.add(Examinations(kind="breast-cancer", title=body["title"], date=body["date"],
                                results=predictions, path=path, username=body["username"]))
        session.commit()

        response = jsonify(success=True)
        response.status_code = 200
        return response
    except:
        response = jsonify(success=False)
        response.status_code = 500
        return response


if __name__ == "__main__":
    app.run(host=config_file["service_address"], port=config_file["service_port"], threaded=True)
