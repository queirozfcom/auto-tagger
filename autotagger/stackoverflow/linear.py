from sklearn import linear_model
from autotagger.helpers.preprocess import load_dataset


# TODO REMEMBER OFF-BY-1 ERROR!
# RECORD N HAS ID N+1

def linear_regression(use_full_dataset=False, num_features=1000):
    X, Y = load_dataset('stackoverflow', use_full_dataset, num_features)

    print(X.shape, Y.shape)
