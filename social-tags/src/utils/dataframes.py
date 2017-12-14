import numpy as np


def sample_rows(source_dataframe, num_samples=None):
    """

    :param source_dataframe:
    :param num_samples:
    :return:
    """
    if num_samples is None:
        num_samples = 100

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
