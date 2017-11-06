import re


def clean_text_bibtex(text):
    """
    remove chars like '{' and '}'

    :param text: all textual features (e.g. title and abstract put together)
    :return:
    """

    return re.sub('{}', '', text)
