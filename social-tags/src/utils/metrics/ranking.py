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


def precision_at_k(y_true, y_score, k=None, normalize=None):
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

    if normalize is None:
        normalize = False

    _validate_inputs(y_true, y_score)

    # just assume the true value is 1 and false is zero
    positive_label = 1

    y_true = _reshape_input(y_true)
    y_score = _reshape_input(y_score)

    # array indices in increasing order
    order_ascending = np.argsort(y_score, axis=1)

    # array indices for highest scores first
    order_descending = np.flip(order_ascending, axis=1)

    score_indices_top_k = order_descending[:, :k]

    # true values for scores that rank highest
    # https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html#integer-array-indexing
    row_indices_to_select = [i for i in range(y_true.shape[0])]
    column_indices_to_select = score_indices_top_k.T

    y_true_top_k = y_true[row_indices_to_select, column_indices_to_select].T

    n_relevant = np.sum(y_true_top_k == positive_label, axis=1).astype(float)

    n_positive = np.sum(y_true == positive_label, axis=1).astype(float)

    # we can use the minimum between k and the number of positive labels
    # as the denominator because there are cases when k 10 but there are
    # only 2 positive labels in y_true so the best possible score should
    # only predict those two even if k is 10.
    k_as_array = np.repeat(k, y_true.shape[0])

    if normalize:
        denominator = np.minimum(k_as_array, n_positive)
    else:
        denominator = k_as_array

    numerator = n_relevant
    # in case we have no predicted labels
    precisions_at_k = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0)

    return precisions_at_k.reshape(-1, 1)


def micro_f1_at_k(y_true, y_score, k=None, normalize=None):
    if k is None:
        k = 10

    if normalize is None:
        normalize = False

    _validate_inputs(y_true, y_score)

    # just assume the true value is 1 and false is zero
    positive_label = 1

    y_true = _reshape_input(y_true)
    y_score = _reshape_input(y_score)

    # array indices in increasing order
    order_ascending = np.argsort(y_score, axis=1)

    # array indices for highest scores first
    order_descending = np.flip(order_ascending, axis=1)

    score_indices_top_k = order_descending[:, :k]

    # true values for scores that rank highest
    # https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html#integer-array-indexing
    row_indices_to_select = [i for i in range(y_true.shape[0])]
    column_indices_to_select = score_indices_top_k.T

    y_true_top_k = y_true[row_indices_to_select, column_indices_to_select].T

    true_positives_at_k = y_true_top_k.astype(int)

    # https://stackoverflow.com/a/17506182/436721
    false_positives_at_k = np.logical_not(true_positives_at_k).astype(int)

    # all other scores which didn't make the top k are implied "negatives"
    # so what we want is the number of positives in y_true bottom n_minus_k
    score_indices_bottom_n_minus_k = order_descending[:, k:]
    column_indices_to_select_2 = score_indices_bottom_n_minus_k.T
    y_true_bottom_n_minus_k = y_true[row_indices_to_select, column_indices_to_select_2].T

    false_negatives_at_k = y_true_bottom_n_minus_k.astype(int)

    sum_tp = true_positives_at_k.sum()
    sum_fn = false_negatives_at_k.sum()
    sum_fp = false_positives_at_k.sum()

    if sum_tp + sum_fn + sum_fp == 0:
        return 0.0
    else:
        if normalize:
            micro_averaged_f1_at_k = (2 * sum_tp) / (2 * sum_tp + sum_fp)
        else:
            micro_averaged_f1_at_k = (2 * sum_tp) / (2 * sum_tp + sum_fn + sum_fp)
        return float(micro_averaged_f1_at_k)


def recall_at_k(y_true, y_score, k=None, normalize=None):
    """
    Out of the positive labels in y_true, how many did
    we correctly return?

    :param y_true:
    :param y_score:
    :param k:
    :return:
    """
    if k is None:
        k = 10

    if normalize is None:
        normalize = False

    _validate_inputs(y_true, y_score)

    # just assume the true value is 1 and false is zero
    positive_label = 1

    y_true = _reshape_input(y_true)
    y_score = _reshape_input(y_score)

    # array indices in increasing order
    order_ascending = np.argsort(y_score, axis=1)

    # array indices for highest scores first
    order_descending = np.flip(order_ascending, axis=1)

    score_indices_top_k = order_descending[:, :k]

    # true values for scores that rank highest
    # https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html#integer-array-indexing
    row_indices_to_select = [i for i in range(y_true.shape[0])]
    column_indices_to_select = score_indices_top_k.T

    y_true_top_k = y_true[row_indices_to_select, column_indices_to_select].T

    n_correct_at_k = np.sum(y_true_top_k == positive_label, axis=1).astype(float)

    n_positive = np.sum(y_true == positive_label, axis=1).astype(float)

    k_as_array = np.repeat(k, y_true.shape[0])
    if normalize:
        denominator = np.minimum(k_as_array, n_positive)
    else:
        denominator = n_positive

    numerator = n_correct_at_k

    # in case we have no true labels
    recalls_at_k = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0)

    return recalls_at_k.reshape(-1, 1)


def f1_score_at_k(y_true, y_score, k=None, normalize=None):
    """

    :param y_true:
    :param y_score:
    :param k:
    :return:
    """
    if k is None:
        k = 10

    if normalize is None:
        normalize = False

    _validate_inputs(y_true, y_score)

    precisions_at_k = precision_at_k(y_true, y_score, k, normalize)
    recalls_at_k = recall_at_k(y_true, y_score, k, normalize)

    numerator = 2 * precisions_at_k * recalls_at_k

    denominator = precisions_at_k + recalls_at_k

    # https://stackoverflow.com/a/37977222/436721
    f1_scores_at_k = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0)

    return f1_scores_at_k.reshape(-1, 1)


def _validate_inputs(y_true, y_score):
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


def _reshape_input(array):
    """

    In case the argument is a 1-d array turn it into
    a row vector (1,x) array.

    And also cast it to float (if it was an int).

    :param indicator_array: numpy array
    :return:
    """

    if len(array.shape) == 1:
        return array.reshape(1, -1).astype(float)
    else:
        return array.astype(float)
