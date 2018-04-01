import numpy as np


def get_word_weight_dict(fitted_model, topic_index, vocabulary):
    word_weights = fitted_model.components_[topic_index]

    tpls = [(vocabulary[i], w) for (i, w) in enumerate(word_weights)]

    return dict(tpls)


def _get_top_words_for_topic(fitted_model, topic_index, vocabulary, n_top_words=None):
    """
    For a given LDA model (trained) and a topic index, return the N most important
    words for that topic.

    :param model: topic model such as sklearn.decomposition.LatentDirichletAllocation
    :param topic_index: 0-indexed integer
    :param vocabulary: list of words in the vocabulary (e.g. call get_feature_names() on a trained
        sklearn.feature_extraction.text.CountVectorizer)
    :param n_top_words: number of words to return. by default, return all
    :return: list of the top words
    """

    topic = fitted_model.components_[topic_index]

    if n_top_words is not None:
        words = [vocabulary[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
    else:
        words = [vocabulary[i] for i in topic.argsort()]

    return words


def _get_word_topic_distribution(lda_model):
    """
    the values in a model component aren't actual conditional word probablities, but rather
    frequency counts. To make it so that each component actually correspond to the distribution
    of words in that topic, we must do the follwoing.

    :param lda_model: topic model such as sklearn.decomposition.LatentDirichletAllocation
    :return:
    """
    return lda_model.components_ / lda_model.components_.sum(axis=1)[:, np.newaxis]
