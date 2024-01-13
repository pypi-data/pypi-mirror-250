import wikipediaapi


def get_first_sentence_wikipedia(article):
    wiki_wiki = wikipediaapi.Wikipedia("geoguesser_knowledge_base/0.1", extract_format=wikipediaapi.ExtractFormat.WIKI)
    wiki_wiki._user_agent = "geoguesser_knowledge_base/0.1"
    page_py = wiki_wiki.page(article)
    if not page_py.exists():
        return f"Wikipedia article for {article} not found."

    first_sentence = remove_text_inside_brackets(page_py.summary).split(".")[0]
    return " "+first_sentence+"."


def remove_text_inside_brackets(text):
    result = ""
    inside_brackets = 0

    for char in text:
        if char == '(':
            inside_brackets += 1
        elif char == ')':
            inside_brackets -= 1
        elif inside_brackets == 0:
            result += char

    return result.strip()+"."
