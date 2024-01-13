# Explanation Text Generator

##### Version of 12th of January 2024

Class to generate text explanations of image classifications 
in different modes and with given main and part labels.

## Main Usage
### Package
The current version of the package can be installed with pip using the following command:
```
pip install ExplanationText==0.1.2
```
The Explanation Generator can then be important with:
```
from explanation_text import ExplanationGenerator
```
After importing the Explanation Generator, the following two lines of code are sufficient.
They are described in more details below:
```
explanation_generator = ExplanationGenerator(<api_token>, <mode>)
explanation_generator.initModels() # optional, loads used models on HuggingFace platform
explanation_text = explanation_generator.generate_explanation(<labels>)
```
First you have to create a ExplanationGenerator and set a explanation mode and 
your [HuggingFace API Token](https://huggingface.co/docs/hub/security-tokens), if you want to use modes that uses their API.
The different explanation modes can be found [here](#ExplanationModes). 
If you leave it empty, the GeoGuesser method will be used. At the beginning of a pipeline, for example after 
the login, the *initModels* function (not in version 0.1.2) can be run in order to load the used language models on the HuggingFace platform,
since the first request often takes some time.
Afterward you can call the *generate_explanation* method with your list of labels
receive an explanation text. In order to generate multiple explanations, 
*generate_explanation* can also handle lists of labels and returns a list 
of individual explanation texts.
You can set two more configurations with the constructor. *MinimumRelevance* (default 10)
filters part labels with a relevance percentage below that value and *maximumPartCount* (default 5)
sets the number of maximum part labels that should be used for the explanation text.

### GeoGuessr Mode Usage

To use the GeoGuessr Mode, the mode has to be set to "ExplanationGeneratorGG". This mode
is currently the default mode, so you don't have to set it manually.
In order to use the Landmark Detection feature with this mode, you also have to provide the
Google API Key in the constructor of the ExplanationGenerator. However, the GeoGuessr
Mode can also be used without Landmark Detection.
```
explanation_generator = ExplanationGenerator(<api_token>, <google_api_token>, "ExplanationGeneratorGG")
```
The Google Vision API Key can be created using a free trial account on [Google Cloud Platform](https://cloud.google.com/apis/docs/getting-started?hl=de).
You simply have to create a new project and enable the Google Vision API. Then you can create
an API key in the credentials section of the project.

## Input Format
The following json files are examples of the current format for the labels that serve as 
input for the explanation generator. 
In addition to the image (img), the input contains a list of objects. Each object has a label,
a heatmap and a list of parts. Optionally, the object can also contain a probability.
Each part contains an image, an optional relevancy, a position and a list of labels.
The labels are a dictionary with a main label as key and a list of part labels as value.
Example Portugal:
```json
{
    "img": "base64",
        "objects" : [
            {
                "heatmap": "image",
                "label": "portugal",
		        "probability": 0.9,
                "parts": [
                  {
                    "img": "base64",
                    "relevancy": 0.3,
                    "rect": "",
                    "labels": {
                      "portugal": [
                        "hills"
                      ]
                    }
                  },
                  {
                    "img": "base64",
                    "relevancy": 0.4,
                    "rect": "",
                    "labels": {
                      "portugal": [
                        "traffic light"
                      ]
                    }
                  },
                                    {
                    "img": "base64",
                    "relevancy": 0.45,
                    "rect": "",
                    "labels": {
                      "portugal": [
                        "building"
                      ]
                    }
                  }
                ]
            }
        ]
    }
```
Example Germany:
```json
{
    "img": "base64",
        "objects" : [
            {
                "heatmap": "image",
                "label": "germany",
		        "probability": 0.9,
                "parts": [
                  {
                    "img": "base64",
                    "relevancy": 0.3,
                    "rect": "",
                    "labels": {
                      "germany": [
                        "apartments"
                      ]
                    }
                  },
                  {
                    "img": "base64",
                    "relevancy": 0.5,
                    "rect": "",
                    "labels": {
                      "germany": [
                        "traffic light"
                      ]
                    }
                  },
                                    {
                    "img": "base64",
                    "relevancy": 0.5,
                    "rect": "",
                    "labels": {
                      "germany": [
                        "building"
                      ]
                    }
                  }
                ]
            }
        ]
    }
```
### Internal Format
After communication with the other groups, a new format came up, that we now
use as the input. Internally, as of September 2023, we parse that format into
our old one you can see below, to make sure all our components still work.
Our internal format of *Labels* is a python dictionary or a list of dictionary objects.
More specifically this object has to contain a non empty key *main_label*, which is the
minimum requirement. Optionally a *probability* with a float value can be set.
Part labels are set as a list with a key *parts*. Each part has to contain a *part_label*
field and optionally a relevance and position.
```json
{
  "objects": [
    {
      "label": "plane", 
      "probability": 0.9, 
      "position": "left",
      "parts": [
        {"part_label": "cockpit", "relevance": 0.6}, 
        {"part_label": "wings", "relevance": 0.2}
       ]
    },
    {
      "label": "tree", 
      "probability": 0.6, 
      "position": "top"
    }
  ]
}
```
This is an example of the label format of an object plane.
Internally the method *generate_explanation* validates, filters and sorts
the given main and part labels.

## Test Bench Usage
To test the different explanation methods, we created a test bench. 
It reads and parses sample labels from a folder with .txt files and creates
explanation texts with a given mode. Additionally, it can randomize the samples
and write the explanations into an output file.
```
demoApiToken = "<Your Huggingface API Token>"
testBench = TestBench('testData', demoApiToken, mode="ExplanationGeneratorV1")
testBench.test_data(100, writeToFile=True, randomize=True)
```
All parameters, except for *inputFolderPath* and *SampleCount* are optional.
If the sample count number is higher than the given samples, the test bench
uses all the samples. The default output folder path is *ExplanationText/output/*
and can be set with an additional parameter *outputPath*.
If parameter mode is set to *All*, all implemented modes will be tested with the
given data.

## Explanation Modes
Here is an overview of the different explanation text modes.

### ExplanationGeneratorV1
This is currently the best mode to generate texts. It follows the structure 
shown in diagram in confluence under 'Language Models' -> 'Umsetzung' -> 'aktueller Stand'
and described in chapter 3 of the 'Zwischenbericht'. To use it, set attribute *mode* to 
'ExplanationGeneratorV1'.

Positive example of current version:
```
    "overview": "This image contains a train, a horse and a boat.",
    "horse": {
        "medium": 
            "The horse in the image was classified as a horse with 
            99% certainty. The horse was mainly classified that 
            way, because of the head with 40% relevance and neck
            with 24% relevance. The head is strongly connected to
            the horse, while the neck is very strongly connected
            to the horse.",
        "detailed": 
            "The main function of the following object is to 
            provide transportation and support to its rider. The 
            object in the image was classified as a horse with a
            99% certainty, due to the distinctive head and neck 
            features. The head was found to have a high relevance,
            as it is a prominent feature of the horse. The neck 
            was also found to be important, as it is connected to
            the head and appears to provide support to the horse."
    },
    ....
```

It is important to notice, that the implementation of component *partConnection* 
is currently faked with random connections.

### ExplanationGeneratorGG
This mode is used to generate Explanation Texts for explanations of 
GeoGuessr images. The structure of the mode and its components can be found in 
the Language Model V3 PDF file.

Example of current version:
```
'overview': 'The image was classified as being located in Germany.', 
'germany': {
    'medium': 
        'The model classified the image as Germany with a high degree of confidence.
         The location of the image was primarily identified based on the presence of 
         a traffic light, a building, and apartments. The relevance of the different
         elements of the image was also taken into consideration, with the traffic light
         having a high relevance, the building having a moderate relevance, and the 
         apartments having a low relevance.', 
    'detailed': 
        'The model classified the image as Germany with a high degree of certainty.
         Germany is a country in the western region of Central Europe. The traffic light
         in the image was relevant for the classification. The image contained buildings
         that had a high relevancy, and the location of the image was identified due to 
         the presence of apartments with a medium relevancy. In urban Germany, apartment 
         buildings are a common sight. They typically line the streets and are three to five
         storeys high. The apartments are usually bland in color and have a simple layout,
         with kitchens, bathrooms, and living rooms on different floors.'
         }
```

### Overview
The mode overview describes only the main labels of an image and should
give an overview of the objects detected. The mode can be set using the string
'Overview'. 
```
The image contains a <main label 1>, .. and a <main label N>.
```
### Sentence Construction
Sentence Construction is the easiest way of creating a detailed explanation text.
It basically just puts the main and part label with additional information into
a fixed sentence structure without any additionally information or processing.
The current variant creates two sentences with the following structure:
```
Object in image was classified as a <main label> with <percentage>%
certainty. The <main label> was mainly classified that way, because
of the <part label> with <percentage>% relevance at position 
<position> , <more part labels> ... and <last part label>
```
The whole second sentence and information about relevance and position are 
optional and will be set if the necessary information is given.
This method can be used with the string 'SentenceConstruction'.

### API Test
API Test is a method to evaluate large language models on [HugginFace](https://huggingface.co/models).
It uses the [HuggingFace API](https://huggingface.co/docs/api-inference/index) to test out sets of models, tasks and prompts.
For this, a *test* can be set up in class [api_test](explanationGenerators/ApiTest/api_test.py) and run with prompts provided by
the Testbench. Examples for test setups can be found in class [api_test_utils](explanationGenerators/api_utils.py).
It is necessary to create an account on HuggingFace and provide a custom API Key at the top of [api_test](explanationGenerators/ApiTest/api_test.py).

This method can be used with the string 'APITest'.
