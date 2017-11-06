def get_top_words_for_topic(model, topic_index, feature_names, n_top_words):
    """
    For a given LDA model (trained) and a topic index, return the N most important
    words for that topic.

    :param model: topic model such as sklearn.decomposition.LatentDirichletAllocation
    :param topic_index: 0-indexed integer
    :param feature_names: list of words in the vocabulary (e.g. call get_feature_names() on a trained
        sklearn.feature_extraction.text.CountVectorizer)
    :param n_top_words: number of words to return
    :return: list of the top words
    """

    topic = model.components_[topic_index]

    words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]

    return words
