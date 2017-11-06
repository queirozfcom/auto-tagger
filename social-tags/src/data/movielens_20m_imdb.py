import pandas as pd
import os
import pickle
import re

from helpers.labels import filter_tag, get_top_unique_tags
from helpers.movielens_imdb import load_movie_plots


def get_from_cache(path_to_movies_file,
                   path_to_tag_assignment_file,
                   path_to_movie_plots_file,
                   interim_data_root):
    if os.path.isfile(interim_data_root.rstrip('/') + "/docs_df.p"):
        docs_df = pickle.load(open(interim_data_root.rstrip('/') + "/docs_df.p", "rb"))
    else:
        raise Exception('cache not set')
        # docs_df = load_into_dataframe(path_to_movies_file,
        #                                path_to_tag_assignment_file,
        #                                path_to_movie_plots_file)
        #
        # pickle.dump(docs_df, open(interim_data_root.rstrip('/') + "/docs_df.p", "wb"))

    return docs_df


def load_into_dataframe(
        path_to_movies_file,
        path_to_tag_assignment_file,
        path_to_movie_plots_file,
        summary_separator=None):
    """

    :param path_to_movies_file:
    :param path_to_tag_assignment_file:
    :param path_to_movie_plots_file:
    :param summary_separator:
    :return: docs dataframe
    """

    if summary_separator is None:
        summary_separator = " "

    # step 1: movie and tags

    movies_df = pd.read_csv(path_to_movies_file,
                            sep=',',
                            skiprows=1,
                            names=[
                                'movie_id', 'title', 'genres'],
                            dtype={
                                'movie_id': 'int64',
                                'title': 'object',
                                'genres': 'object'
                            })

    # there are some duplicated movie titles (in case a movie was
    # re-launched for video or TV) or there was some user error.
    duplicated_titles = movies_df.duplicated(subset=['title'], keep=False)
    movies_df = movies_df[~duplicated_titles]

    # we don't need genres right now
    movies_df = movies_df.drop(['genres'], axis=1)

    tag_assignments_df = pd.read_csv(path_to_tag_assignment_file,
                                     sep=',',
                                     skiprows=1,
                                     names=[
                                         'user_id',
                                         'movie_id',
                                         'tag',
                                         'timestamp'],
                                     dtype={
                                         'user_id': 'int64',
                                         'movie_id': 'int64',
                                         'tag': 'object',
                                         'timestamp': 'object'
                                     })

    # we could drop user ids too but we need it to differentiate among tag assignments
    # to the same movie using the same tag
    tag_assignments_df = tag_assignments_df.drop(['timestamp'], axis=1)

    # add top 25 unique tags for each movie
    docs_df = pd.merge(
        left=movies_df,
        right=(
            tag_assignments_df.groupby("movie_id")["tag"].apply(
                lambda tags: ','.join(get_top_unique_tags([filter_tag(str(t).strip()) for t in tags]))
            ).to_frame().reset_index()
        ),
        on="movie_id",
        how="left"
    ).rename(
        columns={'tag': 'unique_tags'}
    )

    # add num_users
    docs_df = pd.merge(
        left=docs_df,
        right=(
            tag_assignments_df.groupby("movie_id")["user_id"].nunique().to_frame().reset_index()
        ),
        on="movie_id",
        how="left"
    ).rename(
        columns={'user_id': 'num_users'}
    )

    # drop movies with no tags
    docs_df = docs_df[docs_df["unique_tags"].notnull()]

    # add num_tags
    docs_df['num_unique_tags'] = docs_df['unique_tags'].apply(lambda tags: len(tags.split(',')))

    # in delicious-t140 all documents have been tagged by at least
    # 2 users
    docs_df = docs_df[docs_df['num_users'] != 1]

    # in delicious-t140 all documents have at least 2 tags
    docs_df = docs_df[docs_df['num_unique_tags'] != 1]

    unique_movie_titles_movielens = set(docs_df["title"].values)

    # step 2: fetch plots for movies in the dataframe

    plot_dicts = load_movie_plots(path_to_movie_plots_file, unique_movie_titles_movielens,
                                  summary_separator=summary_separator)

    plots_df = pd.DataFrame(columns=['title', 'plot']).astype({'title': 'object', 'plot': 'object'})
    plots_df = plots_df.from_records(plot_dicts)

    # Step 3) join everything and return

    docs_df = pd.merge(
        left=docs_df,
        right=plots_df,
        on="title",
        how="right"
    )

    return docs_df
