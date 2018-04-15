import numpy as np


def sample_rows(source_dataframe, num_samples=None):
    """

    :param source_dataframe:
    :param num_samples: if it's a number between 0 and 1, it's used as the sampling rate. If it's an integer larger than
        1 then it's used as the number of samples to take.
    :return:
    """
    if num_samples is None:
        num_samples = 100
    elif num_samples >0 and num_samples <1.0:
        num_samples = int(len(source_dataframe)*num_samples)
    elif num_samples <= 0:
        raise Exception("num_samples must be a positive number")


    random_indices = np.random.choice(source_dataframe.index.values, num_samples, replace=False)

    # must assign to another variable or the copy doesn't work
    # i.e. return source_dataframe.loc[random_indices]
    # this doesn't really make a copy
    cpy = source_dataframe.loc[random_indices]

    cpy.reset_index(inplace=True)

    # this is needed because when we call reset_index(), the old index
    # stays there with another name
    cpy.drop('index', axis=1, inplace=True)

    return cpy
