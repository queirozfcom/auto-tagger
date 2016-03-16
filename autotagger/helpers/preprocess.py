from pandas import read_csv


def load_dataset(path_to_file, ignore_malformed=True):
    """
    Loads SO dataset into scikit-learn default format for posterior learning.

    A pair (X,Y) is returned. X is an array-like of vector-likes. Each vector-like
    is a feature vector. Y is an array-like of vector-likes. Each vector-like is
    a binary vector representing activated labels.

    Features are extracted using TF-IDF metric.

    :param path_to_file: string
    :param ignore_malformed: boolean
    :return: (samples,labels)
    """


