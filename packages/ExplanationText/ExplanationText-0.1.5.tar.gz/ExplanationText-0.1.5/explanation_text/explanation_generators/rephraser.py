from explanation_text.explanation_generators.api_utils import query_text_generation


def rephrase(mode, input_text, api_token, prompt=None):
    endpoint = "https://api-inference.huggingface.co/models/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}

    if prompt is None:
        prompt = (f"<|prompter|>Paraphrase the following text.\nOriginal: {input_text}\nParaphrase:<|endoftext"
                  f"|><|assistant|>")
    else:
        prompt = f"<|prompter|>{prompt}\nOriginal: {input_text}\nParaphrase:<|endoftext|><|assistant|>"

    if mode == "strict":
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': len(input_text), 'max_time': 120,
                         'num_beams': 3}
    elif mode == "variable":
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': len(input_text), 'max_time': 120.0,
                         'no_repeat_ngram_size': 3, 'num_beams': 5, 'do_sample': True,
                         'top_p': 0.95, 'temperature': 0.6}

    else:
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': len(input_text), 'max_time': 120.0,
                         'no_repeat_ngram_size': 3, 'num_beams': 3, 'do_sample': True,
                         'top_p': 0.92, 'temperature': 0.6}

    query = ["", "", "OpenAssistant/oasst-sft-1-pythia-12b", prompt, configuration]
    (success, return_text) = query_text_generation(query, endpoint, headers)
    if success:
        return return_text

    print(return_text)
    return ""
