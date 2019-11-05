import json


def parse_json_with_predictions_for_skin_lesions(predictions, labels_classes_matcher, customize_printed_value=None):
    predictions = predictions["predictions"][0]
    if customize_printed_value is not None:
        return json.dumps({class_: customize_printed_value(predictions[int(label)]) for label, class_ in labels_classes_matcher.items()})
    else:
        return json.dumps({class_: predictions[int(label)] for label, class_ in labels_classes_matcher.items()})


def to_percent_and_round(value, digits=2):
    return round(100 * value, digits)
