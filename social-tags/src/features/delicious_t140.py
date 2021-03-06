import re


def clean_text_delicious(text):
    step1 = _clean_html(text)

    # this is not the newline character, this is a literal slash and n
    step2 = re.sub('\\n', ' ', step1)

    step3 = re.sub('\s+', ' ', step2)

    return step3


def _clean_html(text):
    """
    Removes html tags from text
    :param text:
    :return:
    """

    # this is the pattern for html tags
    return re.sub('<[^>]+>', '', text)
