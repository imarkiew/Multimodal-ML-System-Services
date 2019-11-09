"""
.. module:: utilities
   :synopsis: Utilities for proxy-server
"""


import json
import base64
import csv
import requests


def parse_predictions_for_skin_lesions(predictions, labels_classes_matcher, customize_printed_value=None):
    """Parse predictions with renaming classes and custom printing of floats if necessary

    :param predictions:
    :param labels_classes_matcher:
    :param customize_printed_value:
    :return: json with parsed results
    """
    predictions = json.loads(predictions)
    predictions = predictions["predictions"][0]
    if customize_printed_value is not None:
        return json.dumps({class_: customize_printed_value(predictions[int(label)]) for label, class_ in labels_classes_matcher.items()})
    else:
        return json.dumps({class_: predictions[int(label)] for label, class_ in labels_classes_matcher.items()})


def parse_predictions_for_breast_cancer(predictions, customize_printed_value=None):
    """Parse predictions with replacing "'" for '"'

    :param predictions:
    :param customize_printed_value:
    :return:
    """
    predictions = json.loads(predictions)
    if customize_printed_value is not None:
        return json.dumps({class_: customize_printed_value(prediction) for class_, prediction in predictions.items()}).replace("'", '"')
    else:
        return json.dumps(predictions).replace("'", '"')


def to_percent_and_round(value, digits=2):
    """Parse value to percents and then round

    :param value: value to parse to percents and round
    :param digits: how many digits after coma we want
    :return: parsed and rounded value
    """
    return round(100 * value, digits)


def get_content(body):
    """ Get content from body and discard metainfo from base64 encoded json

    :param body:
    :return: parsed content
    """
    return body["content"].split(",")[1]


def construct_save_file_path(body, base_file_path):
    """ Concatenate string for save file path

    :param body:
    :param base_file_path:
    :return: String for save file path
    """
    return base_file_path + "/" + body["username"] + "_" + body["fileName"]


def preprocess_content_from_request_body(body, base_file_path="./"):
    """Get content from request body and save it

    :param body:
    :param base_file_path:
    :return: Json with content from request body and path to saved file
    """
    content = get_content(body)
    path = construct_save_file_path(body, base_file_path)

    with open(path, "wb") as f:
        f.write(base64.b64decode(content))

    return content, path


def read_breast_cancer_file(path):
    """Read saved breast cancer file

    :param path:
    :return: Json with data from breast cancer file
    """
    with open(path, "r") as file:
        dict_reader = csv.DictReader(file, delimiter=",")
        dict_raw = list(dict_reader)[0]
        input_dict = {key: float(value) for key, value in dict_raw.items()}
        return json.dumps(input_dict)


def get_response_fom_ml_service(data, path):
    """Get response from ml service

    :param data:
    :param path:
    :return: Response from ml service
    """
    headers = {"content-type": "application/json"}
    return requests.post(path, data=data, headers=headers)
