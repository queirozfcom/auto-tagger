from autotagger.helpers.preprocess import load_dataset


def info():
    print(
            'Lots of examples on multi-label classification for the stackoverflow dataset')


def binary_relevance():
    (X, Y) = load_dataset("/home/felipe/auto-tagger/data/pieces/aa")

    print("Shape of X is {0}\n".format(X.shape))
    print("Shape of Y is {0}\n".format(Y.shape))
