import pandas as pd
import os
import pickle
import re

from helpers.labels import filter_tag,get_top_unique_tags


def load_or_get_from_cache(path_to_movies_file,
                           path_to_tag_assignment_file,
                           path_to_movie_plots_file,
                           interim_data_root):
    if os.path.isfile(interim_data_root.rstrip('/') + "/docs_df.p"):
        docs_df = pickle.load(open(interim_data_root.rstrip('/') + "/docs_df.p", "rb"))
    else:
        docs_df = _load_into_dataframe(path_to_movies_file,
                                       path_to_tag_assignment_file,
                                       path_to_movie_plots_file)

        pickle.dump(docs_df, open(interim_data_root.rstrip('/') + "/docs_df.p", "wb"))

    return docs_df


def _load_into_dataframe(
        path_to_movies_file,
        path_to_tag_assignment_file,
        path_to_movie_plots_file):
    """

    :param path_to_movies_file: format: movieId,title,genres
    :param path_to_tag_assignment_file: format: userId,movieId,tag,timestamp
    :param path_to_movie_plots_file: format: unstructured
    :return: dataframe
    """

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

    plot_dicts = list()

    with open(path_to_movie_plots_file, encoding="ISO-8859-1") as file:

        recording = False
        current_title = None
        current_block_lines = list()

        for (index, line) in enumerate(file):

            # first 15 lines are just metadata
            if index <= 14:
                continue

            if not recording:
                if line.startswith("MV:"):
                    if '(V)' not in line and '(TV)' not in line and '(VG)' not in line and '{{SUSPENDED}}' not in line:
                        # V='video', 'TV'=tv shows, 'VG'= videogames
                        # {{SUSPENDED}} films are always duplicates of other films

                        extracted_title = _extract_title(line)

                        if extracted_title in unique_movie_titles_movielens:
                            current_title = extracted_title
                            recording = True
                            continue

            if line.startswith("-------") and recording == True:
                # reached start of next movie
                recording = False
                block_str = re.sub(' PL:', '', " ".join(current_block_lines))

                current_block_lines = []

                info = {'title': current_title, 'plot': block_str}
                plot_dicts.append(info)

            if recording:
                current_block_lines.append(line.rstrip('\n'))

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


def _extract_title(line_with_title):
    """
    Takes lines starting with "MV:" from the IMDB plot.list file, and extracts
    the actual movie title from this line

    Sample lines:
        MV: Among the Shadows (2014)
        MV: 13 Going on 13 (????) {(#1.2)}
    Extracted Titles:
        Among the Shadows (2014)
        13 Going on 13 (????)

    :param line_with_title:
    :return: title, extracted from given line
    """
    pat_known_date = r'^MV:\s(.+ \(\d{4}(?:/\w{1,3})?\)).*$'
    pat_unknown_date = r'^MV:\s(.+ \(\?\?\?\?(?:/\w{1,3})?\)).*$'

    if re.match(pat_known_date, line_with_title):
        title = re.sub(pat_known_date, r'\1', line_with_title)
    elif re.match(pat_unknown_date, line_with_title):
        title = re.sub(pat_unknown_date, r'\1', line_with_title)
    else:
        title = re.sub(pat_known_date, r'\1', line_with_title)

    title_no_newline = title.rstrip('\n')

    formatted_to_movielens = _format_title_to_movielens_format(title_no_newline)

    return formatted_to_movielens


def _format_title_to_movielens_format(original_title):
    """
    The movielens dataset formats titles starting with articles such as
    'A', 'The' or 'Los', and adds double quotes around it.

    (but some movies stay as is, e.g.: The Butterfly Effect 3: Revelations (2009))

    Example Input:
        The Lazarus Project (2008)
        The Cry (Il Grido) (1957)
        A Hell of a Day (Reines d'un jour) (2001)
    Example Output:
        "Lazarus Project, The (2008)"
        "Cry, The (Grido, Il) (1957)"
        "Hell of a Day, A (Reines d'un jour) (2001)"

    :param original_title:
    :return:
    """
    articles = ["The", "A", "An"]

    # e.g.: "The Lazarus Project (2008)"
    pat_no_subtitle = r'^([^\(]+) (\(\d{4}\))$'

    # e.g. "A Hell of a Day (Reines d'un jour) (2001)"
    pat_with_subtitle = r'^([^\(]+) (\([^\(]+\)) (\(\d{4}\))$'

    pat_first_word_w_space = r'^(\w+ )(.+)$'

    for article in articles:
        if original_title.startswith(article):

            # option 1 - no subtitles
            match = re.match(pat_no_subtitle, original_title)

            if match:
                title = match.group(1)
                year = match.group(2)

                first_word_match = re.match(pat_first_word_w_space, title)

                # believe it or not, there is a movie called 'A'
                if first_word_match:
                    first_word = first_word_match.group(1)

                    title_no_article = re.sub(pat_first_word_w_space, r'\2', title)

                    title_article_in_front = title_no_article + ", " + first_word

                    formatted_title = title_article_in_front + year

                    return '"' + formatted_title + '"'

            # option 2 - with subtitles
            match = re.match(pat_with_subtitle, original_title)

            if match:
                main_title = match.group(1)
                subtitle = match.group(2)
                year = match.group(3)

                first_word_match = re.match(pat_first_word_w_space, main_title)

                # believe it or not, there is a movie called 'A'
                if first_word_match:
                    first_word = first_word_match.group(1)

                    main_title_no_article = re.sub(pat_first_word_w_space, r'\2', main_title)

                    main_title_article_in_front = main_title_no_article + ", " + first_word

                    formatted_title = main_title_article_in_front + subtitle + " " + year

                    return '"' + formatted_title + '"'

    # no match, return original
    return original_title
