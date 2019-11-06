from flask import Flask, request, jsonify
from argparse import ArgumentParser
import json
from scikit_model import Model
from utilities import parse_predictions_for_breast_cancer, get_scaler_params


parser = ArgumentParser()
parser.add_argument("--config_file_path", help="Config file path", type=str, required=True)
parser.add_argument("--config_type", help="Config type", type=str, required=True)
parser.add_argument("--model_file_path", help="File path to model", type=str, required=True)
args = parser.parse_args()
arguments = args.__dict__

with open(arguments["config_file_path"], "r") as file:
    config_file = json.load(file)[arguments["config_type"]]

means, stds = get_scaler_params(config_file["input"])

model = Model(arguments["model_file_path"], means, stds)

app = Flask(__name__)


@app.route("/", methods=["POST"])
def handle_request():
    try:
        predictions = model.predict_proba(request.json)
        response = parse_predictions_for_breast_cancer(predictions, config_file["breast_cancer_labels_classes_matcher"])
        return response
    except:
        response = jsonify(success=False)
        response.status_code = 500
        return response


if __name__ == "__main__":
    app.run(host=config_file["service_address"], port=config_file["service_port"], threaded=True)
