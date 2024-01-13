from explanation_text.explanation_generators.api_utils import query_text_generation
from explanation_text.explanation_generators.explanation_generator_geoguesser.knowledge_base.knowledge_base_controller import \
    (get_prefiltered_information)
from explanation_text.explanation_generators.explanation_generator_geoguesser.knowledge_base.landmark_detection import \
    detect_landmark

import re

endpoint = "https://api-inference.huggingface.co/models/"

landmark_classes = ["building", "monastery", "palace", "residence", "religious residence", "apiary", "boathouse",
                    "place of worship", "church", "mosque", "theater", "cinema", "library", "planetarium", "restaurant",
                    "prison", "institution"]


def generate_part_information(use_landmark_detection, location, part, api_token, google_vision_api_key):
    information = ""
    part_label = str(part.get("part_label")).replace('_', ' ')
    if use_landmark_detection and part_label.lower() in landmark_classes:
        information += detect_landmark(part_label, part.get("img"), google_vision_api_key)
    information += filter_part_information_from_text(location, part_label.replace(' ', '_'), api_token)
    return information


def filter_part_information_from_text(location, part_label, api_token):
    prefiltered_information = get_prefiltered_information(location, part_label, 0.5, 300)
    if len(prefiltered_information) == 0:
        print("  ! Could not find information about " + part_label)
        return ""
    return combine_knowledgebase_information(part_label.replace('_', ' '), prefiltered_information, api_token)


# # Placeholder for Alisas function to combine prefiltered knowledge base information with part
def combine_knowledgebase_information(part_label, part_information, api_token):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}
    prompt = ("<s>[INST] Context: " + part_information
              + ". Merge by context and output information about " + part_label +
              " from given context: [/INST]</s>")

    nr_of_tokens = len(re.findall(r'\w+', part_information))

    configuration = {'return_full_text': False,
                     'max_new_tokens': int(1.3 * nr_of_tokens),
                     'num_return_sequences': 1,
                     'no_repeat_ngram_size': 3,
                     'max_time': 120.0,
                     'num_beams': 3,
                     'do_sample': True,
                     'top_p': 0.92,
                     'temperature': 0.6}

    query = ["", "", "mistralai/Mixtral-8x7B-Instruct-v0.1", prompt, configuration]
    (success, return_text) = query_text_generation(query, endpoint, headers)
    if success:
        return return_text
    else:
        print("! Failed to obtain part information about " + part_label)
        return ""
