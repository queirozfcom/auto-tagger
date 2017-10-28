import pandas as pd
import re


def load_into_dataframe(
        path_to_movies_file,
        path_to_tag_assignment_file,
        path_to_movie_plots_file):
    """

    :param path_to_movies_file: format: MovieID::Title::Genres
    :param path_to_tag_assignment_file: format: UserID::MovieID::Tag::Timestamp
    :param path_to_movie_plots_file: format: unstructured
    :return: dataframe
    """

    # step 1: movie and tags

    movies_df = pd.read_csv(path_to_movies_file, sep='::', engine='python', names=[
        'movie_id', 'title', 'genres'])

    tag_assignments_df = pd.read_csv(path_to_tag_assignment_file,
                                     sep='::',
                                     engine='python',
                                     names=[
                                         'user_id',
                                         'movie_id',
                                         'tag',
                                         'timestamp'])

    docs_df = pd.merge(
        left=movies_df,
        right=(
            tag_assignments_df.groupby("movie_id")["tag"].apply(
                # for some reason it errors if i don't explicitly
                # cast to string
                lambda tags: ','.join(set([str(t) for t in tags]))
            ).to_frame().reset_index()
        ),
        on="movie_id",
        how="left"
    ).rename(
        columns={'tag': 'tags'}
    )

    unique_movie_titles_movielens = set(docs_df["title"].values)

    # step 2: fetch plots for movies in the dataframe

    plot_dicts = list()

    with open(path_to_movie_plots_file, encoding="ISO-8859-1") as file:
        recording = False
        current_title = None
        current_block_lines = list()

        for line in file:

            if not recording:
                if line.startswith("MV:"):

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

    plots_df = pd.DataFrame(columns=['title', 'plot'])
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
        MV: "#BlackLove" (2015) {Bringing Sexy Back (#1.3)}
        MV: "13 Going on 13" (????) {(#1.2)}
        MV: "100% Senorita" (2003/I)

    :param line_with_title:
    :return: title, extracted from given line
    """
    pat_date = r'^MV:\s(.+ \(\d{4}(?:/\w{1,3})?\)).*$'
    pat_unk = r'^MV:\s(.+ \(\?\?\?\?(?:/\w{1,3})?\)).*$'

    if re.match(pat_date, line_with_title):
        title = re.sub(pat_date, r'\1', line_with_title)
    elif re.match(pat_unk, line_with_title):
        title = re.sub(pat_unk, r'\1', line_with_title)
    else:
        title = re.sub(pat_date, r'\1', line_with_title)

    return title.rstrip('\n')
