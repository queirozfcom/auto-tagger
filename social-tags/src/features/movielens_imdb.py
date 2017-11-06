def filter_rare_tags(docs_df, min_doc_df=None):
    """
    remove tags that occur in less than $min_doc_df documents

    :param docs_df:
    :param min_doc_df:
    :return:
    """

    if min_doc_df is None:
        min_doc_df = 1

    tag_sets = docs_df["tags"].values

    all_tags = set()

    for tag_set in tag_sets:
        for tag in tag_set.split(','):
            all_tags.add(tag)
