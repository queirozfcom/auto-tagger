import re, os

from pathlib import Path
from pandas import read_csv
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

_datasets = ['stackoverflow']


def load_dataset(dataset_name, use_full_dataset=False, max_features=1000,
                 ignore_malformed=True):
    """
    Loads multilabel dataset into scikit-learn default format for posterior learning.

    A pair (X,Y) is returned. X is an array-like of vector-likes. Each vector-like
    is a feature vector. Y is an array-like of vector-likes. Each vector-like is
    a binary vector representing activated labels.

    :param dataset_name: string
    :param use_full_dataset: boolean
    :param max_features: integer default 1000
    :param ignore_malformed: boolean
    :return: (samples,labels)
    """

    if dataset_name not in _datasets:
        raise Exception(
                "Bad dataset: {0}. Valid datasets are {1}".format(dataset_name,
                                                                  _datasets))

    if dataset_name == 'stackoverflow':
        return _load_stackoverflow(use_full_dataset, max_features,
                                   ignore_malformed)


        # TODO REMEMBER OFF-BY-1 ERROR!
        # RECORD N HAS ID N+1


def _load_stackoverflow(use_full_dataset, max_features, ignore_malformed):
    if use_full_dataset:
        path = "../../../data/stackoverflow/TrainClean.csv"
    else:
        path = "../../../data/stackoverflow/pieces/aa"

    abs_path = os.path.abspath(__file__ + "/" + path)

    df = read_csv(abs_path,
                  names=['id', 'title', 'body', 'tags'],
                  header=None)

    df["id"] = df["id"].apply(lambda str: str.strip().lstrip('"').rstrip('"'))

    pat = re.compile('<[^>]+>')

    def preprocessor(s):
        return pat.sub(' ', s).lower()

    def tokenizer(s):
        return s.split()

    text_data = df["title"] + ' ' + df["title"] + ' ' + df["body"]

    vectorizerX = TfidfVectorizer(preprocessor=preprocessor,
                                  max_features=max_features)
    X = vectorizerX.fit_transform(text_data.values)

    tag_data = df["tags"]
    token_pattern = '(?u)\b\w+\b'  # allow 1-letter tokens
    vectorizerY = CountVectorizer(tokenizer=tokenizer,
                                  token_pattern=token_pattern,
                                  max_features=max_features)
    Y = vectorizerY.fit_transform(tag_data.values)

    return X, Y
