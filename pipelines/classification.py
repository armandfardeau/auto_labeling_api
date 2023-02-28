from utils.pipelines_helper import from_pipeline
from utils.config import cache


@cache.memoize()
def classify_sequence(sequence, labels, multi_label=False):
    print("Performing text classification for", sequence)
    classifier = from_pipeline("classification")
    classification = classifier(sequence, labels, multi_label=multi_label)
    return classification_output_for(classification, multi_label)


def classification_output_for(classification, multi_label):
    classification_output = {}
    for index, label in enumerate(classification["labels"]):
        classification_output[label] = classification["scores"][index]

    output = {
        "sequence": classification["sequence"],
        "classification": classification_output,
        "labels": classification["labels"],
        "scores": classification["scores"],
    }

    if multi_label:
        return output
    else:
        output["top_classification"] = max(classification_output, key=classification_output.get)
        return output
