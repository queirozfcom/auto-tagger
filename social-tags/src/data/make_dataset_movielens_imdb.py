# -*- coding: utf-8 -*-
import os
import click
import csv
import langid
import logging
import pickle
import re
import sys
from datetime import date
from dotenv import find_dotenv, load_dotenv

from ..helpers.labels import filter_tag


@click.command()
@click.argument('imdb_synopses_file', type=click.Path(exists=True))
@click.argument('movielens_20m_directory', type=click.Path(exists=True))
@click.argument('output_directory', type=click.Path())
def main(imdb_synopses_file, movielens_20m_directory, output_directory):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    TAG_MIN_DF = 5
    MIN_SYNOPSIS_LENGTH = 10

    cwd = os.getcwd()

    path_to_imdb_synopses_file = imdb_synopses_file if os.path.isabs(imdb_synopses_file) else  os.path.abspath(
        cwd + "/" + imdb_synopses_file)

    path_to_movielens_20m_directory = movielens_20m_directory.rstrip("/") if os.path.isabs(
        movielens_20m_directory.rstrip("/")) else os.path.abspath(cwd + "/" + movielens_20m_directory.rstrip("/"))

    path_to_output_directory = output_directory.rstrip("/") if os.path.isabs(
        output_directory.rstrip("/")) else os.path.abspath(cwd + "/" + output_directory.rstrip("/"))

    imdbIdsWithSynopses = set()
    synopses_dict = dict()

    with open(path_to_imdb_synopses_file, "r") as f:
        next(f)

        reader = csv.reader(f, quotechar='"', escapechar='\\', skipinitialspace=True)

        for imdbId, plot_synopsis in reader:

            if plot_synopsis.strip() == "":
                continue
            elif langid.classify(plot_synopsis)[0] != 'en':
                continue
            else:
                imdbIdsWithSynopses.add(imdbId)
                synopses_dict[imdbId] = plot_synopsis



    links_dict = dict()

    with open(path_to_movielens_20m_directory + "/links.csv", "r") as f:
        next(f)

        reader = csv.reader(f, quotechar='"', escapechar='\\', skipinitialspace=True)

        for movieLensId, imdbId, _ in reader:
            links_dict[movieLensId] = imdbId

    movie_titles_dict = dict()

    with open(path_to_movielens_20m_directory + "/movies.csv", "r") as f:
        next(f)

        reader = csv.reader(f, quotechar='"', escapechar='\\', skipinitialspace=True)

        for movieLensId, title, _ in reader:
            if links_dict[movieLensId] in imdbIdsWithSynopses:
                movie_titles_dict[movieLensId] = title

    movie_tags_dict = dict()
    tag_movies_dict = dict()

    with open(path_to_movielens_20m_directory + "/tags.csv", "r") as f:
        next(f)

        reader = csv.reader(f, quotechar='"', doublequote=True, skipinitialspace=True)

        for userId, movieLensId, tag, _ in reader:

            if links_dict[movieLensId] not in imdbIdsWithSynopses:
                continue

            tag_filtered = filter_tag(tag)

            if movie_tags_dict.get(movieLensId) is None:
                movie_tags_dict[movieLensId] = set([tag_filtered])
            else:
                tags = movie_tags_dict[movieLensId]
                tags.add(tag_filtered)
                movie_tags_dict[movieLensId] = tags

            if tag_movies_dict.get(tag_filtered) is None:
                tag_movies_dict[tag_filtered] = set([movieLensId])
            else:
                movies = tag_movies_dict[tag_filtered]
                movies.add(movieLensId)
                tag_movies_dict[tag_filtered] = movies

    out_rows = []

    for i,(movieLensId, title) in enumerate(movie_titles_dict.items()):
        imdbId = links_dict[movieLensId]

        if links_dict[movieLensId] not in imdbIdsWithSynopses:
            continue

        synopsis = synopses_dict[imdbId]

        unique_tags = [tag for tag in movie_tags_dict.get(movieLensId, []) if tag != ""]

        unique_tags = [tag for tag in unique_tags if len(tag_movies_dict[tag]) >= TAG_MIN_DF ]

        if len(unique_tags) == 0:
            continue

        if len(synopsis) <= MIN_SYNOPSIS_LENGTH:
            continue

        unique_tags_as_text = ",".join(unique_tags)

        num_tags = len(unique_tags)

        out_rows.append(
            {'movie_id': movieLensId, 'title': title, 'synopsis': synopsis, 'tags': unique_tags_as_text, "num_tags": num_tags})

    # make sure the output file carries the base date
    date_pattern = "^[^\.]+(\d{4}-\d{2}-\d{2})\.[^\.]+$"

    matches = re.match(date_pattern, imdb_synopses_file)

    if matches:
        reference_date = matches.group(1)

        path_to_output_file = path_to_output_directory + "/movielens-20m-imdb-tags-and-synopses-" + \
                              reference_date + ".csv"

        with open(path_to_output_file, 'w') as fout:
            csv_writer = csv.DictWriter(fout,
                                        fieldnames=["movie_id", "title", "synopsis", "tags", "num_tags"],
                                        escapechar='\\',  # escape double quotes using a single backslash
                                        doublequote=False,  # don't duplicate every double quote
                                        quoting=csv.QUOTE_ALL)  # wrap every value in double quotes, for safety
            csv_writer.writeheader()

            for row in out_rows:
                csv_writer.writerow(row)

    else:
        print("input file name does not have a date in the name."
              "It should be something like: 'my-file-2017-01-01.csv'")
        sys.exit()


def main2(imdb_synopses_file, movielens_20m_directory, output_directory):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    cwd = os.getcwd()

    path_to_imdb_synopses_file = imdb_synopses_file if os.path.isabs(imdb_synopses_file) else  os.path.abspath(
        cwd + "/" + imdb_synopses_file)

    path_to_movielens_20m_directory = movielens_20m_directory.rstrip("/") if os.path.isabs(
        movielens_20m_directory.rstrip("/")) else os.path.abspath(cwd + "/" + movielens_20m_directory.rstrip("/"))

    path_to_output_directory = output_directory.rstrip("/") if os.path.isabs(
        output_directory.rstrip("/")) else os.path.abspath(cwd + "/" + output_directory.rstrip("/"))

    use_cache = True

    if use_cache:
        imdbIdsWithSynopses = pickle.load(open("imdbIdsWithSynopses.p", "rb"))
        synopses_dict = pickle.load(open("synopses_dict.p", "rb"))
        links_dict = pickle.load(open("links_dict.p", "rb"))
        movie_titles_dict = pickle.load(open("movie_titles_dict.p", "rb"))
    else:
        imdbIdsWithSynopses = set()
        synopses_dict = dict()

        with open(path_to_imdb_synopses_file, "r") as f:
            next(f)

            reader = csv.reader(f, quotechar='"', escapechar='\\', skipinitialspace=True)

            for imdbId, plot_synopsis in reader:

                if plot_synopsis.strip() == "":
                    continue
                elif langid.classify(plot_synopsis)[0] != 'en':
                    continue
                else:
                    imdbIdsWithSynopses.add(imdbId)
                    synopses_dict[imdbId] = plot_synopsis

        links_dict = dict()

        with open(path_to_movielens_20m_directory + "/links.csv", "r") as f:
            next(f)

            reader = csv.reader(f, quotechar='"', escapechar='\\', skipinitialspace=True)

            for movieLensId, imdbId, _ in reader:
                links_dict[movieLensId] = imdbId

        movie_titles_dict = dict()
        with open(path_to_movielens_20m_directory + "/movies.csv", "r") as f:
            next(f)

            reader = csv.reader(f, quotechar='"', escapechar='\\', skipinitialspace=True)

            for movieLensId, title, _ in reader:
                if links_dict[movieLensId] in imdbIdsWithSynopses:
                    movie_titles_dict[movieLensId] = title

        pickle.dump(imdbIdsWithSynopses, open("imdbIdsWithSynopses.p", "wb"))
        pickle.dump(synopses_dict, open("synopses_dict.p", "wb"))
        pickle.dump(links_dict, open("links_dict.p", "wb"))
        pickle.dump(movie_titles_dict, open("movie_titles_dict.p", "wb"))

    use_cache = True

    if use_cache:
        movie_tags_dict = pickle.load(open("movie_tags_dict.p", "rb"))
        tag_movies_dict = pickle.load(open("tag_movies_dict.p", "rb"))
        movie_users_dict = pickle.load(open("movie_users_dict.p", "rb"))
        user_movies_dict = pickle.load(open("user_movies_dict.p", "rb"))
        tag_users_dict = pickle.load(open("tag_users_dict.p", "rb"))
        user_tags_dict = pickle.load(open("user_tags_dict.p", "rb"))
    else:

        movie_tags_dict = dict()
        tag_movies_dict = dict()
        movie_users_dict = dict()
        user_movies_dict = dict()
        tag_users_dict = dict()
        user_tags_dict = dict()

        with open(path_to_movielens_20m_directory + "/tags.csv", "r") as f:
            next(f)

            reader = csv.reader(f, quotechar='"', doublequote=True, skipinitialspace=True)

            for userId, movieLensId, tag, _ in reader:

                tag_filtered = filter_tag(tag)

                if links_dict[movieLensId] in imdbIdsWithSynopses:
                    if movie_tags_dict.get(movieLensId) is None:
                        movie_tags_dict[movieLensId] = set(tag_filtered)
                    else:
                        tags = movie_tags_dict[movieLensId]
                        tags.add(tag_filtered)
                        movie_tags_dict[movieLensId] = tags

                if links_dict[movieLensId] in imdbIdsWithSynopses:
                    if tag_movies_dict.get(tag_filtered) is None:
                        tag_movies_dict[tag_filtered] = set(movieLensId)
                    else:
                        movies = tag_movies_dict[tag_filtered]
                        movies.add(movieLensId)
                        tag_movies_dict[tag_filtered] = movies

                if links_dict[movieLensId] in imdbIdsWithSynopses:
                    if movie_users_dict.get(movieLensId) is None:
                        movie_users_dict[movieLensId] = set(userId)
                    else:
                        users = movie_users_dict[movieLensId]
                        users.add(userId)
                        movie_users_dict[movieLensId] = users

                if links_dict[movieLensId] in imdbIdsWithSynopses:
                    if user_movies_dict.get(userId) is None:
                        user_movies_dict[userId] = set(movieLensId)
                    else:
                        movies = user_movies_dict[userId]
                        movies.add(movieLensId)
                        user_movies_dict[userId] = movies

                if links_dict[movieLensId] in imdbIdsWithSynopses:
                    if tag_users_dict.get(tag_filtered) is None:
                        tag_users_dict[tag_filtered] = set(userId)
                    else:
                        users = tag_users_dict[tag_filtered]
                        users.add(userId)
                        tag_users_dict[tag_filtered] = users

                if links_dict[movieLensId] in imdbIdsWithSynopses:
                    if user_tags_dict.get(userId) is None:
                        user_tags_dict[userId] = set(tag_filtered)
                    else:
                        tags = user_tags_dict[userId]
                        tags.add(tag_filtered)
                        user_tags_dict[userId] = tags

        pickle.dump(movie_tags_dict, open("movie_tags_dict.p", "wb"))
        pickle.dump(tag_movies_dict, open("tag_movies_dict.p", "wb"))
        pickle.dump(movie_users_dict, open("movie_users_dict.p", "wb"))
        pickle.dump(user_movies_dict, open("user_movies_dict.p", "wb"))
        pickle.dump(tag_users_dict, open("tag_users_dict.p", "wb"))
        pickle.dump(user_tags_dict, open("user_tags_dict.p", "wb"))

    out_rows = []

    # post-core-2 pruning

    for i in range(10):

        documents_dropped = 0
        total_documents = len(movie_titles_dict.keys())

        for movieLensId, title in movie_titles_dict.items():

            # print("movielensId:{}".format(movieLensId))

            imdbId = links_dict[movieLensId]
            if imdbId in imdbIdsWithSynopses:
                synopsis = synopses_dict[imdbId]

                current_tags = [tag for tag in movie_tags_dict.get(movieLensId, set())]

                current_users = [user for user in movie_users_dict.get(movieLensId, set())]

                updated_tags = [tag for tag in current_tags if tag in tag_users_dict.keys() and
                                tag in tag_movies_dict.keys()]

                updated_users = [user for user in current_users if user in user_movies_dict.keys() and
                                 user in user_tags_dict.keys()]

                # all_tags are already unique
                # unique_tags = set(all_tags)

                movie_tags_dict[movieLensId] = updated_tags
                movie_users_dict[movieLensId] = updated_users

                movie_titles_dict_updated = movie_titles_dict.copy()

                # if my tags reached zero, remove myself from all users and tags that pointed to me
                if len(updated_tags) <= 1:
                    copied = tag_movies_dict.copy()
                    del movie_tags_dict[movieLensId]

                    for tag, movieId in tag_movies_dict.items():
                        if movieId == movieLensId:
                            movies = tag_movies_dict[tag]
                            movies.remove(movieLensId)

                            if len(movies) == 0:
                                del copied[tag]
                            else:
                                copied[tag] = movies

                    movie_tags_dict = copied

                    copied = user_movies_dict.copy()
                    for userId, movieId in user_movies_dict.items():
                        if movieId == movieLensId:
                            movies = user_movies_dict[userId]
                            movies.remove(movieLensId)

                            if len(movies) == 0:
                                del copied[userId]
                            else:
                                copied[userId] = movies

                    user_movies_dict = copied

                    del movie_titles_dict_updated[movieLensId]
                    documents_dropped += 1
                    continue

                if len(updated_users) <= 1:

                    del movie_tags_dict[movieLensId]

                    for tag, movieId in tag_movies_dict.items():
                        if movieId == movieLensId:
                            copied = tag_movies_dict.copy()
                            movies = tag_movies_dict[tag]
                            movies.remove(movieLensId)

                            if len(movies) == 0:
                                del copied[tag]
                            else:
                                copied[tag] = movies

                    movie_tags_dict = copied

                    for userId, movieId in user_movies_dict.items():
                        if movieId == movieLensId:
                            copied = user_movies_dict.copy()
                            movies = user_movies_dict[userId]
                            movies.remove(movieLensId)

                            if len(movies) == 0:
                                del copied[userId]
                            else:
                                copied[userId] = movies

                    user_movies_dict = copied

                    del movie_titles_dict_updated[movieLensId]
                    documents_dropped += 1
                    continue

        movie_titles_dict = movie_titles_dict_updated

        print("iteration {}: total documents: {},  documents dropped: {}".format(i, total_documents, documents_dropped),
              sep='')

        print("")

    sys.exit("early..")

    for movieLensId, title in movie_titles_dict.items():
        imdbId = links_dict[movieLensId]
        if imdbId in imdbIdsWithSynopses:
            synopsis = synopses_dict[imdbId]

            all_tags = [filter_tag(tag) for tag in movie_tags_dict.get(movieLensId, [])]

            unique_tags = set(all_tags)

            all_tags_as_text = ",".join(all_tags)

            unique_tags_as_text = ",".join(unique_tags)

            num_users = len(movie_users_dict.get(movieLensId, set()))

    out_rows.append(
        {'movie_id': movieLensId, 'title': title, 'synopsis': synopsis, 'all_tags': all_tags_as_text,
         'unique_tags': unique_tags_as_text, 'num_users': num_users})

    # make sure the output file carries the base date
    date_pattern = "^[^\.]+(\d{4}-\d{2}-\d{2})\.[^\.]+$"

    matches = re.match(date_pattern, imdb_synopses_file)

    if matches:
        reference_date = matches.group(1)

        path_to_output_file = path_to_output_directory + "/movielens-20m-imdb-tags-and-synopses-" + \
                              reference_date + ".csv"

        with open(path_to_output_file, 'w') as fout:
            csv_writer = csv.DictWriter(fout,
                                        fieldnames=["movie_id", "title", "synopsis", "all_tags"],
                                        escapechar='\\',  # escape double quotes using a single backslash
                                        doublequote=False,  # don't duplicate every double quote
                                        quoting=csv.QUOTE_ALL)  # wrap every value in double quotes, for safety
            csv_writer.writeheader()

            for row in out_rows:
                csv_writer.writerow(row)

    else:
        print("input file name does not have a date in the name")
        sys.exit()


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
