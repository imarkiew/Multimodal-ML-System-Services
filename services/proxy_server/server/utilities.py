"""
.. module:: utilities
   :synopsis: Utilities for proxy-server
"""


import json


def parse_json_with_predictions_for_skin_lesions(predictions, labels_classes_matcher, customize_printed_value=None):
    """Parse predictions with renaming classes and custom printing of floats if necessary

    :param predictions:
    :param labels_classes_matcher:
    :param customize_printed_value:
    :return: json with parsed results
    """
    predictions = predictions["predictions"][0]
    if customize_printed_value is not None:
        return json.dumps({class_: customize_printed_value(predictions[int(label)]) for label, class_ in labels_classes_matcher.items()})
    else:
        return json.dumps({class_: predictions[int(label)] for label, class_ in labels_classes_matcher.items()})


def to_percent_and_round(value, digits=2):
    """Parse value to percents and then round

    :param value: value to parse to percents and round
    :param digits: how many digits after coma we want
    :return: parsed and rounded value
    """
    return round(100 * value, digits)
