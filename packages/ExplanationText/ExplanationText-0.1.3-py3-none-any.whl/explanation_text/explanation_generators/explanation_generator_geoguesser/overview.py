import random

# sentence templates

overview_sentences = ["The location of the image was classified as {0}."]

# Removed sentence "The view was classified as {0}."


def generate_overview_text(location):
    """
    Method to generate overview text for GeoGuesser
    """

    if len(location) != 1:
        return "There was a problem with the classification of the image."

    return random.choice(overview_sentences).format(location[0])
