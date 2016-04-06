from __future__ import print_function
from autotagger.stackoverflow.preprocess import \
    load_stackoverflow_partial_sklearn_format


def info():
    print(
            'Lots of examples on multi-label classification for the stackoverflow dataset')


def binary_relevance():
    (X, Y) = load_stackoverflow_partial_sklearn_format()

    print("Shape of X is {0}\n".format(X.shape))
    print("Shape of Y is {0}\n".format(Y.shape))
