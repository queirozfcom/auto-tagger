import pandas as pd
import xml.etree.ElementTree as ET
from joblib import Parallel, delayed

# read the tag-assignment file (taginfo.xml) into a dataframe
def load_taginfo_into_dataframe(input_filepath):
    tree = ET.parse(input_filepath)

    dataset = tree.getroot()

    elements = Parallel(n_jobs=-1)(delayed(__get_attribute_dict_from_document_node)(document) for document in dataset)

    docs_df = pd.DataFrame.from_records(elements)

    docs_df['num_tags'] = docs_df['tags'].apply(lambda tags: len(tags.split(',')))
    docs_df.rename(columns={'users': 'num_users'}, inplace=True)
    docs_df['num_users'] = docs_df['num_users'].astype('int64')
    docs_df['num_tags'] = docs_df['num_tags'].astype('int64')

    docs_df = docs_df[docs_df["filetype"] == "html"].reindex()

    return docs_df


# def load_individual_content(input_filepath):




def __get_attribute_dict_from_document_node(document):
    attrs_dict = dict()

    for attribute_node in document:

        tags = []

        if attribute_node.tag == 'tags':
            for tag_node in attribute_node:
                for subnode in tag_node:
                    if subnode.tag == 'name':
                        if subnode.text is not None:
                            tags.append(subnode.text)

            attrs_dict['tags'] = ','.join(tags)

        else:
            attrs_dict[attribute_node.tag] = attribute_node.text

    return attrs_dict

