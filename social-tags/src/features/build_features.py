import re

from nltk.tokenize import StanfordTokenizer


def clean_text(text):
    return _clean(text)


def _clean(text):
    # this is the pattern for html tags
    step1 = re.sub('<[^>]+>', '', text)

    # this is not the newline character, this is a literal slash and n
    step2 = re.sub('\\n',' ', step1)

    step3 = re.sub('\s+',' ', step2)

    return step3


def _tokenize(text):
    OPTIONS = {'ptb3Escaping': False}

    return StanfordTokenizer(options=OPTIONS).tokenize(text)
