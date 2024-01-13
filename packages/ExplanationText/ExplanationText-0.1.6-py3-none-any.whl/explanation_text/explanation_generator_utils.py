"""
File with general utility functions for the explanation generator
"""


def validate_and_parse_image(image, minimum_relevance, maximum_part_count):
    """
    Function to parse, validate and sort content of labels dictionary
    """
    if 'objects' not in image or image.get('objects') == "":
        return [], []

    object_list = []
    new_objects = []
    objects = image.get('objects')
    all_probabilities_given = True

    for single_object in objects:

        if 'label' not in single_object or single_object.get('label') == "":
            break

        object_list.append(single_object.get('label'))
        if 'probability' in single_object:
            single_object.update({'probability': float_to_percentage(single_object.get('probability'))})
        else:
            all_probabilities_given = False

        if 'parts' not in single_object:
            break

        if 'heatmap' in single_object:
            del single_object['heatmap']

        if 'parts' not in single_object or len(single_object.get('parts')) < 1:
            single_object.pop('parts')
        else:
            # parse part labels
            parts = single_object.get('parts')
            sorted_parts = []
            for part in parts:
                if 'labels' in part and single_object.get('label') in part.get('labels') \
                        and len(part.get('labels').get(single_object.get('label'))) > 0:
                    new_part = {
                        "part_label": create_sentence_from_list(part.get('labels').get(single_object.get('label')))}
                    if 'img' in part:
                        new_part.update({'img': part.get('img')})
                    if 'relevancy' in part:
                        try:
                            # Check if relevance is greater than minimum relevance
                            relevance = float_to_percentage(part.get('relevancy'))
                            if relevance >= minimum_relevance:
                                new_part.update({'relevance': relevance})
                                sorted_parts.append(new_part)
                        except ValueError:
                            print(str(part.get('relevance')
                                      + " is not a valid value for relevance in object "
                                      + single_object.get('label')))
                    else:
                        sorted_parts.append(new_part)
                else:
                    pass
                    # print(part.get('labels'))

            # Sort part labels
            sorted_parts = sorted(sorted_parts, key=lambda d: d['relevance'], reverse=True)
            if len(sorted_parts) > 0:
                single_object.update({'parts': sorted_parts[:maximum_part_count]})
            else:
                single_object.pop('parts')

        new_objects.append(single_object)

    if all_probabilities_given:
        # Sort objects
        sorted_objects = sorted(new_objects, key=lambda d: d['probability'], reverse=True)
        return object_list, sorted_objects

    return object_list, new_objects


def float_to_percentage(a):
    """
    Method parse float string to percentage string
    """
    try:
        if 0 < a < 1:
            return round(float(a) * 100)

        return 100
    except ValueError:
        return 0


def create_sentence_from_list(word_list):
    """
    Method to parse a list of labels to a string
    of the format <label1>, <label2>, ... and <labelN>
    """
    if not word_list:
        return ""

    if len(word_list) == 1:
        return word_list[0]

    sentence = ", ".join(word_list[:-1]) + " and " + word_list[-1]
    return sentence


def dict_to_lowercase(input_data):
    """
    Function to lowercase input data
    """
    if isinstance(input_data, dict):
        # If the input is a dictionary, recursively convert keys and values to lowercase
        return {key.lower(): dict_to_lowercase(value) for key, value in input_data.items()}
    elif isinstance(input_data, list):
        # If the input is a list, recursively convert elements to lowercase
        return [dict_to_lowercase(item) for item in input_data]
    elif isinstance(input_data, tuple):
        # If the input is a tuple, recursively convert elements to lowercase
        return tuple(dict_to_lowercase(item) for item in input_data)
    elif isinstance(input_data, str):
        # If the input is a string, convert it to lowercase
        return input_data.lower()
    else:
        # For other types, return as is
        return input_data
