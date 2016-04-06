from __future__ import print_function
import os
import re
import pickle
from pandas import read_csv
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# TODO test if files exist prior to returning

_path = "../../../data/stackoverflow/"


def load_pickle_sklearn_format(name):
    """
    Loads a previously saved pickle file

    :param name: string the name of the pickle file
    :return: (samples,labels)
    """

    path_X = os.path.abspath(__file__ + "/" + _path + "/pickles/" + name + "_X")
    path_Y = os.path.abspath(__file__ + "/" + _path + "/pickles/" + name + "_Y")

    X = pickle.load(open(path_X, 'rb'))
    Y = pickle.load(open(path_Y, 'rb'))

    return X, Y


def load_stackoverflow_partial_sklearn_format(max_features=1000):
    """
    Loads multilabel dataset into scikit-learn default format for posterior learning.

    A pair (X,Y) is returned. X is an array-like of vector-likes. Each vector-like
    is a feature vector. Y is an array-like of vector-likes. Each vector-like is
    a binary vector representing activated labels.

    :param max_features: integer default 1000
    :return: (samples,labels)
    """

    abs_path = os.path.abspath(__file__ + "/" + _path + "/pieces/aa")

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
