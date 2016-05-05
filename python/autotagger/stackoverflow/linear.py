from __future__ import print_function
from sklearn import linear_model
from autotagger.stackoverflow.preprocess import \
    load_stackoverflow_partial_sklearn_format

# TODO REMEMBER OFF-BY-1 ERROR!
# RECORD N HAS ID N+1

def linear_regression(use_full_dataset=False, max_features=1000):
    X, Y = load_stackoverflow_partial_sklearn_format(max_features)

    print(X.shape, Y.shape)
