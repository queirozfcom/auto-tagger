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

    return source_dataframe.loc[random_indices]
