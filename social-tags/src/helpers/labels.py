import re
import string
from collections import OrderedDict


def filter_tag(tag):
    """
    cleans a tag (removes all punctuation and replaces spaces with dashes)

    (inspired by https://github.com/ktsaurabh/recursive_WSABIE/blob/master/tag_embeddings_test_rsdae.py)

    :param tag: possibly badly formatted tag
    :return: clean tag
    """

    # string.punctuation is the same as '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    punct = string.punctuation

    # keep single quotes and underscores
    punct = punct.replace("'", '')
    punct = punct.replace("_", '')

    punctuation_pattern = '[' + punct + ']'

    no_punctuation = re.sub(punctuation_pattern, '', tag)

    clean_tag = re.sub('\s+', '-', no_punctuation)

    return clean_tag.lower()


def get_top_unique_tags(tags_assigned, k=None):
    """
    given a list with potential duplicates, return the top K unique
    tags in the list.

    Sample input:
        ['foo','bar','foo','bar','baz','quux']
    Sample output (for k=2):
        ['foo','bar']

    :param tags_assigned:
    :param k: number of unique tags to keep
    :return: top unique tags
    """
    if k is None:
        k = 25

    count_dict = OrderedDict()

    for tag in tags_assigned:

        if count_dict.get(tag) is None:
            count_dict[tag] = 1
        else:
            count_dict[tag] = count_dict[tag] + 1

    sorted_items = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

    top_sorted = sorted_items[:k]

    return [x[0] for x in top_sorted]


def truncate_labels(labels, min_doc_count):
    """
    labels is an array of label sets.

    remove labels that occur in less than min_doc_count documents

    :param labels: list of lists
    :param min_doc_count: integer
    :return:
    """

    if min_doc_count == 0:
        return labels

    label_index = dict()

    for label_row in labels:

        for label in label_row:
            if label_index.get(label) is None:
                label_index[label] = 1
            else:
                label_index[label] = label_index[label] + 1

    good_labels = []

    for label, doc_count in label_index.items():
        if doc_count >= min_doc_count:
            good_labels.append(label)

    new_labels = []

    for label_row in labels:
        new_labels.append([label for label in label_row if label in good_labels])

    return new_labels
