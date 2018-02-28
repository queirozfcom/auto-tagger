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

    TAG_MIN_DF = 10
    MIN_SYNOPSIS_LENGTH = 10

    cwd = os.getcwd()

    path_to_imdb_synopses_file = imdb_synopses_file if os.path.isabs(imdb_synopses_file) else os.path.abspath(
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

        ## IMPORTANT (cleaning the raw text prior to saving the preprocessed version)
        synopsis1 = synopses_dict[imdbId]
        synopsis = synopsis1.replace(r'\n\n',' ')

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

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
