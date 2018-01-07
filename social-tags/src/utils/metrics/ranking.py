# Based on a code snippet by Mathieu Blondel, available online at https://gist.github.com/mblondel/7337391
# (C) Mathieu Blondel, November 2013
# (C) Felipe Almeida, November 2017
# License: BSD 3 clause

import numpy as np


# original code
def ranking_precision_score(y_true, y_score, k=None):
    """Precision at rank k
    Parameters
    ----------
    y_true : array-like, shape = [n_samples]
        Ground truth (true relevance labels).
    y_score : array-like, shape = [n_samples]
        Predicted scores.
    k : int
        Rank.
    Returns
    -------
    precision @k : float
    """
    unique_y = np.unique(y_true)

    if len(unique_y) > 2:
        raise ValueError("Only supported for two relevance levels.")

    # edited by felipe:
    # just assume the true value is 1 and false is zero
    # otherwise we get errors when, for instance, the label array is [1,1,1,1]
    # pos_label = unique_y[1]

    pos_label = 1
    n_pos = np.sum(y_true == pos_label)

    order = np.argsort(y_score)[::-1]
    y_true = np.take(y_true, order[:k])
    n_relevant = np.sum(y_true == pos_label)

    # Divide by min(n_pos, k) such that the best achievable score is always 1.0.
    return float(n_relevant) / min(n_pos, k)


def precision_at_k(y_true, y_score, k=None):
    """Precision at rank k. Same as above but with support for multiple dimensions at the
    same time.

    Parameters
    ----------
    y_true : array-like, shape = [n_samples,n_labels]
        Ground truth (binary) (true relevance labels)
    y_score : array-like, shape = [n_samples,n_labels]
        Predicted scores (float) (label probabilities)
    k : int
        Rank.
    Returns
    -------
    precision @k : float
    """
    if k is None:
        k = 10

    assert y_true.shape == y_score.shape, "Y_true (binary label vectors) and" + \
                                          "y_preds (predicted probability" + \
                                          "scores) must have the same shapes."

    unique_y = np.unique(y_true.ravel())

    if len(unique_y) > 2:
        raise ValueError("Only supported for two relevance levels (binary " +
                         "indicator arrays).")

    valid_elements = [0, 1]

    unique_elements = np.unique(unique_y)
    elements_are_valid = [True if elem in valid_elements else False for elem in unique_elements]

    if not np.array(elements_are_valid).all():
        raise ValueError("y_true must be a binary indicator ndarray")

    # just assume the true value is 1 and false is zero
    positive_label = 1

    y_true = _normalize_array(y_true)
    y_score = _normalize_array(y_score)

    # array indices in increasing order
    order_ascending = np.argsort(y_score, axis=1)

    # array indices for highest scores first
    order_descending = np.flip(order_ascending, axis=1)

    score_indices_top_k = order_descending[:, :k]

    # true values for scores that rank highest
    # https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html#integer-array-indexing
    row_indices_to_select = [i for i in range(y_true.shape[0])]
    column_indices_to_select = score_indices_top_k.T

    y_true_top_k = y_true[row_indices_to_select,column_indices_to_select].T

    n_relevant = np.sum(y_true_top_k == positive_label, axis=1).astype(float)

    precisions_at_k = n_relevant / k

    return precisions_at_k.reshape(-1, 1)


def ranking_recall_score(y_true, y_score, k=None):
    # TODO
    pass


def ranking_f1_score(y_true, y_score, k=None):
    # TODO
    pass


def _normalize_array(indicator_array):
    """

    In case the argument is a 1-d array turn it into
    a row vector (1,x) array.

    And also cast it to float (if it was an int).

    :param indicator_array: numpy array
    :return:
    """

    if len(indicator_array.shape) == 1:
        return indicator_array.reshape(1, -1).astype(float)
    else:
        return indicator_array.astype(float)
