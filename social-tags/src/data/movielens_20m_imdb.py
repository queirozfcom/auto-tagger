import csv
import pandas as pd
import os
import pickle

from helpers.labels import filter_tag, get_top_unique_tags
from helpers.movielens_imdb import load_movie_plots


def load_df_or_get_from_cache(path_to_file, interim_data_root):

    if os.path.isfile(interim_data_root.rstrip('/') + "/docs_df.p"):
        docs_df = pickle.load(open(interim_data_root.rstrip('/') + "/docs_df.p", "rb"))
    else:
        docs_df = _load_into_dataframe(path_to_file)
        pickle.dump(docs_df, open(interim_data_root.rstrip('/') + "/docs_df.p", "wb"))

    return docs_df


def _load_into_dataframe(path_to_file):
    """

    :param path_to_movies_file:
    :return: docs dataframe
    """

    # step 1: movie and tags

    movies_df = pd.read_csv(path_to_file,
                            skiprows=1,
                            escapechar='\\',  # escape double quotes using a single backslash
                            doublequote=False,  # don't duplicate every double quote,
                            quotechar='"',
                            quoting=csv.QUOTE_ALL,
                            names=[
                                'movie_id', 'title', 'synopsis', 'tags','num_tags'],
                            dtype={
                                'movie_id': 'int64',
                                'title': 'object',
                                'synopsis': 'object',
                                'tags': 'object',
                                "num_tags": "int32"
                            })


    # there may be some duplicated movie titles (in case a movie was
    # re-launched for video or TV) or there was some user error.
    duplicated_titles = movies_df.duplicated(subset=['title'], keep='first')
    movies_df = movies_df[~duplicated_titles]

    movies_df = movies_df.sort_values('movie_id').reset_index().drop('index',axis=1)

    # stick to the standard name
    docs_df = movies_df

    return docs_df
