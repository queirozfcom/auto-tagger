import numpy as np

from src.utils.distances import hausdorff

def make_distance_matrix_for_segments(vectorized_segments, distance='hausdorff'):
    """
    Returns the distance matrix for the documents having the given segments.

    :param vectorized_segments: array of size M, where each element is a "bag" of segments: matrix of
        shape (*,NUM_FEATURES), and each row on this matrix is the TF-IDF vector for one segment.
    :param distance: how to compare the two bags
    :return: pairwise distance matrix (MxM matrix)
    """
    if distance.lower().strip() != 'hausdorff':
        raise Exception("Only 'hausdorff' distance supported right now.")

    num_samples = len(vectorized_segments)

    distance_function = lambda a, b: hausdorff(a.toarray(), b.toarray())

    distance_matrix = np.zeros((num_samples, num_samples))

    for i, segments_for_document_a in enumerate(vectorized_segments):
        for j, segments_for_document_b in enumerate(vectorized_segments):
            distance = distance_function(segments_for_document_a, segments_for_document_b)
            distance_matrix[i][j] = distance

    return distance_matrix


def vectorize_segments(segments, vectorizer):
    """
    Turn each segment into a bag-of-words array using the provided vectorizer.

    :param segments: array of size M, where each element is a "bag" of segments, i.e. a list of
        strings.
    :param vectorizer: instance of CountVectorizer, TfIdfvectorizer, etc.
    :return: vectorized segments (array of size M where each element is a matrix)
    """
    vectorized_segments_list = []

    for segments in segments:
        vectorized = vectorizer.transform(segments)
        vectorized_segments_list.append(vectorized)

    vectorized_segments = np.array(vectorized_segments_list)

    return vectorized_segments
