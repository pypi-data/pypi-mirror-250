import base64
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

from explanation_text.explanation_generators.explanation_generator_geoguesser.knowledge_base.wikipedia import \
    get_first_sentence_wikipedia


def detect_landmark(part_label, image, api_key):
    if api_key != "":

        client = vision_v1.ImageAnnotatorClient(client_options={"api_key": api_key})

        image_content = base64.b64decode(image + '=' * (len(image) % 4))

        image = types.Image(content=image_content)

        response = client.landmark_detection(image=image)
        landmarks = response.landmark_annotations

        if landmarks:
            landmark = landmarks[0].description
            print("  ! Landmark {0} detected.".format( landmark))
            part_information = "The {0} was detected as {1}.".format(part_label, landmark)
            part_information += get_first_sentence_wikipedia(landmark)
            return part_information + " "
        else:
            print(response)
            print("  ! No Landmark detected.")
            return ""

    print("ERROR: No API Key for google vision api set")
    return ""
