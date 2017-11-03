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
