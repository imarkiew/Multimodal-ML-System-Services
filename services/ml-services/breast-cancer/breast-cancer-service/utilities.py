"""
.. module:: utilities
   :synopsis: Utilities for breast-cancer-service
"""


import numpy as np
import json


def get_scaler_params(json_array):
    """Get scaler parameters from json array

    :param json_array: json array with scaler parameters
    :return: Map with scaler parameters
    """
    means = {}
    stds = {}
    for feature in json_array:
        means[feature["name"]] = feature["offset"]
        stds[feature["name"]] = feature["scaling"]
    return means, stds


def parse_predictions_for_breast_cancer(predictions, labels_classes_matcher, customize_printed_value=None):
    """Parse predictions with renaming classes and custom printing of floats if necessary

    :param predictions:
    :param labels_classes_matcher:
    :param customize_printed_value:
    :return: json with parsed results
    """
    predictions = predictions[0]
    if customize_printed_value is not None:
        predictions = np.array(customize_printed_value(value) for value in predictions)
    predictions = {labels_classes_matcher[str(index)]: value for index, value in enumerate(predictions)}
    return json.dumps(predictions)
