import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from joblib import Parallel, delayed
import pickle
import os
import gc

from src.helpers.labels import filter_tag, truncate_labels
from src.helpers.delicious_t140 import load_contents, make_path_to_file
from src.features.delicious_t140 import clean_text_delicious


def get_sample_from_cache(interim_data_root,sample_frac):
    full_path = interim_data_root.rstrip('/') + "/docs_df_with_clean_content_SAMPLE_FRAC_{}_SEED_42.p".format(sample_frac)

    if os.path.isfile(full_path):
        docs_df = pickle.load(open(full_path, "rb"))
        return docs_df
    else:
        raise FileNotFoundError(full_path)


def get_full_from_cache(interim_data_root, with_contents=None):
    if with_contents is None:
        with_contents = False

    if with_contents:
        full_path = interim_data_root.rstrip('/') + "/docs_df_with_content.p"
    else:
        full_path = interim_data_root.rstrip('/') + "/docs_df_no_content.p"

    if os.path.isfile(full_path):
        docs_df = pickle.load(open(full_path, "rb"))
        return docs_df
    else:
        raise FileNotFoundError(full_path)


def load_or_get_from_cache(path_to_file, interim_data_root):
    TAG_MIN_DF = 10

    if os.path.isfile(interim_data_root.rstrip('/') + "/docs_df_no_content.p"):
        docs_df = pickle.load(open(interim_data_root.rstrip('/') + "/docs_df_no_content.p", "rb"))
    else:
        tree = ET.parse(path_to_file)

        dataset = tree.getroot()

        elements = Parallel(n_jobs=-1)(
            delayed(__get_attribute_dict_from_document_node)(document) for document in dataset)

        docs_df = pd.DataFrame.from_records(elements)

        # TRUNCATE LABELS HERE
        labels = docs_df["tags"].map(lambda tagstring: tagstring.split(","))
        labelsets = truncate_labels(labels, TAG_MIN_DF)
        joined_labelsets = [",".join(labelset) for labelset in labelsets]

        docs_df["tags"] = joined_labelsets

        docs_df = docs_df[docs_df["filetype"] == "html"].reindex()

        docs_df['num_tags'] = docs_df['tags'].apply(lambda tags: len(tags.split(',')))
        docs_df.rename(columns={'users': 'num_users'}, inplace=True)
        docs_df['num_users'] = docs_df['num_users'].astype('int64')
        docs_df['num_tags'] = docs_df['num_tags'].astype('int64')

        pickle.dump(docs_df, open(interim_data_root.rstrip('/') + "/docs_df_no_content.p", "wb"))

    return docs_df


def load_or_get_from_cache_with_contents(source_dataframe, interim_data_root, data_root, sample_frac=None):
    """
    extracts a random sample of source_dataframe and loads text contents for each document in the sampled dataframe.

    :param source_dataframe: the full delicious-t140 dataframe, with document tags and IDs, but no contents yet
        or None if you just want to use this method to load the dataset with contents from cache
    :param interim_data_root: path to the directory where interim data is kept. This is our cache directory.
    :param data_root: path to the directory where the original files were downloaded, or None if you just want
        to use this method to load the dataset with contents from disk
    :param sample_frac: sample fraction. default is 1.0 or 100%
    :return: a sample
    """
    if sample_frac is None:
        sample_frac = 1.0

    if os.path.isfile(interim_data_root.rstrip('/') + "/docs_df_with_content.p"):
        loaded_dataframe = pickle.load(open(interim_data_root.rstrip('/') + "/docs_df_with_content.p", "rb"))

        random_indices = np.random.choice(loaded_dataframe.index.values, int(len(loaded_dataframe) * sample_frac),
                                          replace=False)

        sample_df_src = loaded_dataframe.loc[random_indices]

        # https://stackoverflow.com/a/27680109/436721
        sample_df = sample_df_src.reset_index().drop(['index'], axis=1).copy()

    else:
        random_indices = np.random.choice(source_dataframe.index.values, int(len(source_dataframe) * sample_frac),
                                          replace=False)

        sample_df = source_dataframe.loc[random_indices]
        sample_df = sample_df.reset_index().drop(['index'], axis=1)
        sample_df['contents'] = sample_df['hash'].map(
            lambda hash: clean_text_delicious(load_contents(make_path_to_file(data_root, hash))))

        pickle.dump(sample_df, open(interim_data_root.rstrip('/') + "/docs_df_with_content.p", "wb"))

    return sample_df


# read the tag-assignment file (taginfo.xml) into a dataframe
# no contents
def __get_attribute_dict_from_document_node(document):
    attrs_dict = dict()

    for attribute_node in document:

        # each unique tag is only counted once
        tags = set()

        if attribute_node.tag == 'tags':
            for tag_node in attribute_node:
                for subnode in tag_node:
                    if subnode.tag == 'name':
                        if subnode.text is not None:
                            tag_text = subnode.text
                            tags.add(filter_tag(tag_text).strip())

            attrs_dict['tags'] = ','.join(tags)
        else:
            attrs_dict[attribute_node.tag] = attribute_node.text

    return attrs_dict
