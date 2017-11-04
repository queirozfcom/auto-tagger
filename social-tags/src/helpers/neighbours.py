import numpy as np


def get_predicted_labels_from_neighbours(neighbour_labels, neighbour_distances, weights=None):
    """
    Returns the predicted labels (as a binary indicator array) for an instance, based upon
    the given neighbour_labels and neighbour_distances.

    If weights is 'distance', each neighbour's vote will be inversely proportional to
    the distance between that neighbour and the target instance. If weights is 'uniform',
    all neighbors have equal vote.

    :param neighbour_labels: 2d numpy ndarray
    :param neighbour_distances: 1d numpy ndarray
    :param weights: either 'distance' or 'uniform'
    :return:
    """

    assert (neighbour_labels.shape[0] == len(neighbour_distances))

    if weights is None:
        weights = 'distance'
    elif weights not in ['distance', 'uniform']:
        raise Exception("accepted weights: 'distance' or 'uniform', got: '{}'".format(weights))

    predicted_votes = np.zeros(neighbour_labels.shape[1], dtype='float64')

    if weights == 'distance':

        for (i, label_set) in enumerate(neighbour_labels):
            distance = neighbour_distances[i]

            positive_votes = label_set / (1+distance)

            negative_label_set = np.array([1 if elem == 0.0 else 0 for elem in label_set])

            negative_votes = negative_label_set / (1+distance)

            predicted_votes += positive_votes

            predicted_votes -= negative_votes

    else:

        for (i, label_set) in enumerate(neighbour_labels):
            distance = neighbour_distances[i]

            positive_votes = label_set

            negative_label_set = np.array([1 if elem == 0.0 else 0 for elem in label_set])

            negative_votes = negative_label_set

            predicted_votes += positive_votes

            predicted_votes -= negative_votes

    predicted_labels = [1 if elem > 0 else 0 for elem in predicted_votes]

    return predicted_labels