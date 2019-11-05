import numpy as np
import json


def get_scaler_params(json_array):
    means = {}
    stds = {}
    for feature in json_array:
        means[feature["name"]] = feature["offset"]
        stds[feature["name"]] = feature["scaling"]
    return means, stds


def parse_predictions_for_breast_cancer(predictions, labels_classes_matcher, customize_printed_value=None):
    predictions = predictions[0]
    if customize_printed_value is not None:
        predictions = np.array(customize_printed_value(value) for value in predictions)
    predictions = {labels_classes_matcher[str(index)]: value for index, value in enumerate(predictions)}
    return json.dumps(predictions)
