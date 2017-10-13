import re

from nltk.tokenize import StanfordTokenizer


def clean_text_delicious(text):
    return _clean_html(text)

def clean_text_bibtex(text):
    """
    remove chars like '{' and '}'

    :param text: all textual features (e.g. title and abstract put together)
    :return:
    """

    return re.sub('{}','',text)


def clean_text_bookmark(text):
    pass




def _clean_html(text):
    # this is the pattern for html tags
    step1 = re.sub('<[^>]+>', '', text)

    # this is not the newline character, this is a literal slash and n
    step2 = re.sub('\\n',' ', step1)

    step3 = re.sub('\s+',' ', step2)

    return step3


def _tokenize(text):
    OPTIONS = {'ptb3Escaping': False}

    return StanfordTokenizer(options=OPTIONS).tokenize(text)
