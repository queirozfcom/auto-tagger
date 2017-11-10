import re


def load_movie_plots(
        path_to_movie_plots_file,
        existing_movie_titles,
        summary_separator):
    """

    :param path_to_movie_plots_file:
    :param existing_movie_titles:
    :param summary_separator:
    :return:
    """

    plot_dicts = list()

    with open(path_to_movie_plots_file, encoding="ISO-8859-1") as file:

        recording = False
        current_title = None
        current_movie_text = ""

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

                        if extracted_title in existing_movie_titles:
                            current_title = extracted_title
                            recording = True
                            continue

            if line.startswith("-------") and recording:
                # reached start of next movie
                recording = False

                clean_movie_text = re.sub(r"\s*PL:\s*", ' ', current_movie_text.strip())

                current_movie_text = ""

                info = {'title': current_title, 'plot': clean_movie_text.strip()}
                plot_dicts.append(info)

            if recording:

                # lines starting with 'BY: ' signal the end of a specific plot summary
                # in which case we should add the summary_separator and ignore the contents
                # of the line itself.
                if line.startswith('BY:'):
                    current_movie_text = current_movie_text.strip() + summary_separator
                else:
                    current_movie_text = current_movie_text.strip() + " " + line.rstrip('\n').strip()

    return plot_dicts


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
