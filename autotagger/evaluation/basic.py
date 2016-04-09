from __future__ import division

import numpy as np


def build_dummy_pred_test_pair():
    """
    builds a dummy pair of binary multilabel predictions and actual labels, whose
    micro-averaged f1 score must equal 0.7

    :return: micro f1 score
    """

    pred_y = [
        [1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 0, 1]
    ]

    test_y = [
        [1, 0, 1, 1, 0],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1]
    ]

    return np.array(pred_y), np.array(test_y)


def get_micro_f1(predictions, test_set):
    assert len(predictions) == len(
            test_set), "there must be an equal number of elements in both sets"

    sum_f1 = 0
    num_elements = len(predictions)

    for pred, test in zip(predictions, test_set):
        p = __get_precision(pred, test)
        r = __get_recall(pred, test)

        sum_f1 += (2 * p * r) / (p + r)

    if num_elements == 0:
        return 0
    else:
        return sum_f1 / num_elements


def __get_precision(predictions, test_set):
    assert predictions.ndim == 1
    assert test_set.ndim == 1
    assert predictions.shape == test_set.shape, "predicted and test array-likes must have the same shape"
    assert all(prediction == 1 or prediction == 0 for prediction in
               predictions), "predictions must be binary"
    assert all(elem == 1 or elem == 0 for elem in
               test_set), "predictions must be binary"

    num_relevant_retrieved = 0
    num_retrieved = 0

    for idx, elem in enumerate(predictions):
        if elem == 1:
            num_retrieved += 1
            if test_set[idx] == 1:
                num_relevant_retrieved += 1

    if num_retrieved == 0:
        return 0
    else:
        return num_relevant_retrieved / num_retrieved


def __get_recall(predictions, test_set):
    assert predictions.ndim == 1
    assert test_set.ndim == 1
    assert predictions.shape == test_set.shape, "predicted and test array-likes must have the same shape"
    assert all(prediction == 1 or prediction == 0 for prediction in
               predictions), "predictions must be binary"
    assert all(elem == 1 or elem == 0 for elem in
               test_set), "predictions must be binary"

    num_relevant_retrieved = 0
    num_relevant = 0

    for idx, elem in enumerate(test_set):
        if elem == 1:
            num_relevant += 1
            if predictions[idx] == 1:
                num_relevant_retrieved += 1

    if num_relevant == 0:
        return 0
    else:
        return num_relevant_retrieved / num_relevant
