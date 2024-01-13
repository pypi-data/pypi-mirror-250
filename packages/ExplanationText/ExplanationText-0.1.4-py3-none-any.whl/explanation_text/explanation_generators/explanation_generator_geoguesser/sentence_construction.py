import random

# Sentence templates

main_sentences = ["The image was classified as {0}.", "The location of the image was classified as {0}.",
                  "The model classified the image as {0}.", "The model classified the location of the image as {0}.",
                  "The image was most likely taken in {0}."]

main_sentences_with_probability = ["The image was classified as {0} with {1}% certainty.",
                                   "The location of the image was classified as {0} with {1}% probability.",
                                   "The location of the image was classified as {0} with {1}% certainty.",
                                   "The model classified the image as {0} with {1}% certainty.",
                                   "The model classified the image as {0} with {1}% confidence."]

part_sentences = ["The location was identified because of the {0} in the image.",
                  "The location was identified due to the {0} in the image.",
                  "{0} was/were detected in the image.",
                  "The image contained {0}.", "The classification was influenced by {0} in the image.",
                  "The {0} in the image influenced the classification.",
                  "The {0} in the image influenced the classification decision.",
                  "The model's decision was influenced by {0} in the image.",
                  "{0} was/were relevant for the identification of the location.",
                  ]

part_sentences_with_relevancy = \
    ["The location of the image was identified due to the {0} with {1}% relevancy.",
     "The {0} that was/were detected in the image had {1}% relevancy for the classification.",
     "The {0} in the image had {1}% relevancy for the classification.",
     "The {0} in the image was {1}% relevant for the classification.",
     "The {0} in the image was {1}% relevant for the classification decision.",
     "The image contained {0} that had {1}% relevancy.",
     "With {1}% relevancy the classification was influenced by {0}."]


def generate_sentence_construction_medium(single_object):
    """
    Method for medium explanation with sentence construction for GeoGuesser
    Gets random main sentence from list with fixed part sentences.s
    """

    explanation = generate_main_label_explanation(single_object)

    # part labels sentence
    if 'parts' not in single_object:
        return explanation[:-1]

    # Start of the second sentence
    part_explanation = " The location was mainly identified that way, because of the "

    # sentence part for each part label
    for part in single_object.get('parts'):

        part_label = part.get('part_label')
        part_explanation += str(part_label)

        if 'relevance' in part:
            relevance = part.get('relevance')
            part_explanation += " with " + str(relevance) + "% relevance"
        part_explanation += ", "

    # fix format of last part explanation and return explanation
    explanation += format_explanation(part_explanation, single_object)

    return explanation


def generate_main_label_explanation(single_object):
    """
    Method to construct main label sentence
    """

    if len(single_object) < 1:
        return ""
    location = single_object.get('label')

    if 'probability' in single_object:
        probability = single_object.get('probability')
        return random.choice(main_sentences_with_probability).format(location, probability)
    else:
        return random.choice(main_sentences).format(location)


def generate_part_label_explanation(part):
    """
    Method to construct part label sentence
    """
    part_label = part.get('part_label').replace('_', ' ')

    if 'relevance' in part:
        relevance = part.get('relevance')
        return random.choice(part_sentences_with_relevancy).format(part_label, relevance)

    return random.choice(part_sentences).format(part_label)


def format_explanation(explanation, single_object):
    """
    Method fix format issues with last part explanation sentence.
    Add dot at the end and replace last comma with 'and'.
    """
    if explanation.endswith(" "):
        explanation = explanation[:-2] + "."

    if 'parts' in single_object:
        last_comma_index = explanation.rfind(",")
        explanation = explanation[:last_comma_index] + " and" + explanation[last_comma_index + 1:]

    return explanation


def float_to_percentage(a):
    """
    Method parse float string to percentage string
    """
    try:
        return str(round(float(a) * 100))
    except ValueError:
        return "0.0"
