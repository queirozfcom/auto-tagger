import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from joblib import Parallel, delayed
import pickle
import os

from helpers.labels import filter_tag
from helpers.delicious_t140 import load_contents, make_path_to_file


def load_or_get_from_cache(path_to_file, interim_data_root):
    if os.path.isfile(interim_data_root.rstrip('/') + "/docs_df_old.p"):
        docs_df = pickle.load(open(interim_data_root.rstrip('/') + "/docs_df_old.p", "rb"))
    else:
        docs_df = _load_taginfo_into_dataframe(path_to_file)
        pickle.dump(docs_df, open(interim_data_root.rstrip('/') + "/docs_df_old.p", "wb"))

    return docs_df


def make_sample_with_contents_or_get_from_cache(source_dataframe, interim_data_root, data_root, sample_frac=None):
    """
    extracts a random sample of source_dataframe and loads text contents for each document in the sampled dataframe.

    :param source_dataframe: the full delicious-t140 dataframe, with document tags and IDs, but no contents yet
    :param interim_data_root: path to the directory where interim data is kept
    :param data_root: path to the directory where the original files were downloaded
    :param sample_frac: sample fraction. default is 0.1
    :return: a sample
    """
    if sample_frac is None:
        sample_frac = 0.1

    if os.path.isfile(interim_data_root.rstrip('/') + "/sample_df.p"):
        sample_df = pickle.load(open(interim_data_root.rstrip('/') + "/sample_df.p", "rb"))
    else:
        random_indices = np.random.choice(source_dataframe.index.values, int(len(source_dataframe) * sample_frac),
                                          replace=False)

        sample_df = source_dataframe.loc[random_indices]
        sample_df = sample_df.reset_index().drop(['index'], axis=1)
        sample_df['contents'] = sample_df['hash'].map(lambda hash: load_contents(make_path_to_file(data_root, hash)))

        pickle.dump(sample_df, open(interim_data_root.rstrip('/') + "/sample_df.p", "wb"))

    return sample_df


# read the tag-assignment file (taginfo.xml) into a dataframe
# no contents
def _load_taginfo_into_dataframe(input_filepath):
    tree = ET.parse(input_filepath)

    dataset = tree.getroot()

    elements = Parallel(n_jobs=-1)(delayed(__get_attribute_dict_from_document_node)(document) for document in dataset)

    docs_df = pd.DataFrame.from_records(elements)

    docs_df['num_unique_tags'] = docs_df['unique_tags'].apply(lambda tags: len(tags.split(',')))
    docs_df.rename(columns={'users': 'num_users'}, inplace=True)
    docs_df['num_users'] = docs_df['num_users'].astype('int64')
    docs_df['num_unique_tags'] = docs_df['num_unique_tags'].astype('int64')

    # there are only 2 guys with one single tag assigned (out of 144,000)
    # I'll take them out and then consider that the dataset only has documents
    # with at least 2 different tags given (probably noise)
    docs_df = docs_df[docs_df['num_unique_tags'] != 1]

    # similarly, only 1 document has been tagged by only one user
    # I'll take that out too, since it's probably noise.
    docs_df = docs_df[docs_df['num_users'] != 1]

    docs_df = docs_df[docs_df["filetype"] == "html"].reindex()

    return docs_df


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

            attrs_dict['unique_tags'] = ','.join(tags)
        else:
            attrs_dict[attribute_node.tag] = attribute_node.text

    return attrs_dict
