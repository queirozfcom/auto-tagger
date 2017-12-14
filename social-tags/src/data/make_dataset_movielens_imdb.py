# -*- coding: utf-8 -*-
import os
import click
import csv
import langid
import logging
from datetime import date
from dotenv import find_dotenv, load_dotenv


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
    with open(path_to_movielens_20m_directory + "/tags.csv", "r") as f:
        next(f)

        reader = csv.reader(f, quotechar='"', doublequote=True, skipinitialspace=True)

        for userId, movieLensId, tag, _ in reader:

            if links_dict[movieLensId] in imdbIdsWithSynopses:
                if movie_tags_dict.get(movieLensId) is None:
                    movie_tags_dict[movieLensId] = [tag]
                else:
                    movie_tags_dict[movieLensId] = movie_tags_dict[movieLensId] + [tag]

    out_rows = []

    for movieLensId, title in movie_titles_dict.items():
        imdbId = links_dict[movieLensId]
        if imdbId in imdbIdsWithSynopses:
            synopsis = synopses_dict[imdbId]
            tags = ",".join(tag for tag in movie_tags_dict.get(movieLensId, []))

            if tags.strip() == "":
                continue

            out_rows.append({'movie_id': movieLensId, 'title': title, 'synopsis': synopsis, 'all_tags': tags})

    todays_date = date.today().isoformat()

    path_to_output_file = path_to_output_directory + "/movielens-20m-imdb-tags-and-synopses-{}.csv".format(todays_date)

    with open(path_to_output_file, 'w') as fout:
        csv_writer = csv.DictWriter(fout,
                                    fieldnames=["movie_id", "title", "synopsis", "all_tags"],
                                    escapechar='\\',  # escape double quotes using a single backslash
                                    doublequote=False,  # don't duplicate every double quote
                                    quoting=csv.QUOTE_ALL)  # wrap every value in double quotes, for safety
        csv_writer.writeheader()

        for row in out_rows:
            csv_writer.writerow(row)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
