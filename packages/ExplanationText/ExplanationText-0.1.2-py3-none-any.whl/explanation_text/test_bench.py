import json
import os
import random
from datetime import datetime
from explanation_generator_main import ExplanationGenerator


class TestBench:
    """
    A testbench class that reads data from a file and provides a testData method to
    test the ExplanationText implementation automatically
    """

    def __init__(self, input_folder_path, api_token="", google_api_token="", mode="ExplanationGeneratorV1",
                 output_path="output"):
        """
        Constructor for the testbench class, calls read_data method and sets in- and output folder paths
        """
        self.folder_path = input_folder_path
        self.output_path = output_path
        self.mode = mode
        self.samples = self.read_data()
        self.mode_description = str(self.mode)
        self.image_max_size = 5
        self.image_size = random.randint(1, self.image_max_size)
        self.api_token = api_token
        self.google_api_token = google_api_token

    def load_api_keys_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if "huggingface_api_key" in data and "google_vision_api_key" in data:
                    self.api_token = data.get("huggingface_api_key")
                    self.google_api_token = data.get("google_vision_api_key")
                else:
                    print("Error: The file should contain exactly two password key-value pairs.")
                    return None
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file '{file_path}': {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def read_data(self):
        """
        Method to read data from all .txt files in a given folder return as a list
        """
        print("Start reading data from files")
        data = []
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                        data.extend([line.strip() for line in lines])
        print("Data from files read")
        return data

    def write_output(self, explanations, filename):
        """
        Method to write explanation into output .txt file
        """
        output_folder_exists = os.path.exists(self.output_path)
        if not output_folder_exists:
            print("Directory for output " + str(self.output_path) + " does not exist")
            os.makedirs(self.output_path)
            print("New output directory is created")
        file_path = os.path.join(self.output_path, filename + ".txt")
        with open(file_path, 'x') as f:
            if not isinstance(explanations, list):
                explanations = [explanations]
            for explanation in explanations:
                f.write(json.dumps(explanation, indent=4, ensure_ascii=False) + '\n')

    def test_data(self, object_count, randomize=True, write_to_file=False):
        """
        Method to test sample labels with given length and optional randomization
        and optional write into output file
        """

        # catch a too big sample count
        if object_count > len(self.samples) or object_count < 1:
            print("Length of testdata is smaller then desired number of test samples or below 1.")
            object_count = len(self.samples)

        # get test data sample
        test_data = []
        if randomize:
            for i in range(object_count):
                x = random.sample(self.samples, 1)
                test_data.append(x[0])
        else:
            for i in range(min(object_count, len(self.samples))):
                test_data.append(self.samples[i])

        # parse test data sample
        parsed_test_data = self.parse_test_data(test_data)
        print("Test Data parsed")
        # print(json.dumps(parsed_test_data, indent=3))

        # generate explanations
        explanations = []
        explanations.extend(["--- Explanations for Mode: " + self.mode_description + " ---"])
        explanations.extend(self.generate_explanations(parsed_test_data))

        # write in output file
        if write_to_file:
            print("Writing into output file..")
            now = datetime.now()
            filename = now.strftime("explanation_%d%m%Y_%H%M%S")
            self.write_output(explanations, filename)
            print("Explanations written into file " + str(filename))

    def generate_explanations(self, parsed_test_data):
        explanation_generator = ExplanationGenerator(mode=self.mode, api_token=self.api_token,
                                                     google_api_token=self.google_api_token)
        print("Init HuggingFace Language Models")
        explanation_generator.initModels()
        print("\nStart testing samples with mode " + str(self.mode_description))

        explanations = []
        average_times = []
        print(f"Testing {len(parsed_test_data)} samples")
        for test_sample in parsed_test_data:
            explanation, average_time = explanation_generator.generate_explanation(test_sample, return_time=True)
            print(json.dumps(explanation, indent=4, ensure_ascii=False))
            print("")
            explanations.append(explanation)
            average_times.append(average_time)

        total_average_time = round(sum(average_times) / len(average_times), 2)
        print(f"All samples tested with an total average of {str(total_average_time)} seconds per object")
        return explanations

    def parse_test_data(self, data):
        """
        Method to parse raw text line from text file into list of main label and part label
        """
        object_list = []
        unusable_count = 0

        # for each line of read data
        for sample in data:
            sample_split = sample.split(";")
            if len(sample_split) == 0 or sample_split[0] == "":
                unusable_count += 1
            else:

                # Parse main label and probability
                split = sample_split[0].split(",")
                main_label = split[0]
                new_sample = {'heatmap': 'base64', 'label': main_label}

                if len(split) > 1:
                    probability = split[1].replace(",", ".")
                    try:
                        probability = float(probability)
                        new_sample.update({'probability': probability})
                    except ValueError:
                        pass

                sample_split.pop(0)

                # Parse each part label
                part_label_list = []
                for part_label in sample_split:
                    split = part_label.split(",")
                    if len(split) > 0 and not split[0] == "":
                        new_part_label = {"img": "base64", "rect": "(0, 0, 0, 0)",
                                          'labels': {main_label: [split[0][1:]]}}

                        # Optionally add relevance and position
                        if len(split) > 1:
                            relevance = split[1].replace(",", ".")
                            try:
                                relevance = float(relevance)
                                new_part_label.update({'relevancy': relevance})
                            except ValueError:
                                pass
                        if len(split) > 2:
                            new_sample.update({'position': split[2][1:]})

                        part_label_list.append(new_part_label)

                        new_sample.update({'parts': part_label_list})
                object_list.append(new_sample)

        if unusable_count > 0:
            print(str(unusable_count) + " samples where unusable")

        image_list = []
        while len(object_list) >= 1:
            if len(object_list) < self.image_size:
                image_list.append({"image": "base64", "objects": object_list})
                break
            objects = []
            for _ in range(self.image_size):
                objects.append(object_list.pop(0))
            image_list.append({"image": "base64", "objects": objects})
            self.image_size = random.randint(1, self.image_max_size)
        return image_list

    def test_json_file(self, file_path, write_to_file):
        """
        Method to test explanation generator with json file
        """

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                # generate explanations
                explanations = []
                explanations.extend(["--- Explanations for Mode: " + self.mode_description + " ---"])
                explanations.extend(self.generate_explanations([data]))

                # write in output file
                if write_to_file:
                    print("Writing into output file..")
                    now = datetime.now()
                    filename = now.strftime("explanation_%d%m%Y_%H%M%S")
                    self.write_output(explanations, filename)
                    print("Explanations written into file " + str(filename))

        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except json.JSONDecodeError as e:
            print(f"Error decoding the JSON file '{file_path}': {e}")


# TestBench Demo

testBench = TestBench('test_data', mode="ExplanationGeneratorGG")
testBench.load_api_keys_from_file("api_keys.json")
# testBench.test_data(10, write_to_file=True, randomize=True)
# testBench.test_json_file("test_data/app_group_tests/7/processeddictionary.json", True)
testBench.test_json_file("test_data/geoguesser_demo3.json", False)
