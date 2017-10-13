import pandas as pd


def load_bibtex_and_tags(bibtex_filepath, tas_filepath):
    bibtex_df = pd.read_csv(bibtex_filepath, sep='\t', error_bad_lines=False, names=[
        'content_id', 'journal', 'volume', 'chapter', 'edition', 'month', 'day', 'booktitle', 'howPublished',
        'institution', 'organization', 'publisher', 'address', 'school', 'series', 'bibtexKey', 'url', 'type',
        'description', 'annote',
        'note', 'pages', 'bKey', 'number', 'crossRef', 'misc', 'bibtexAbstract', 'hash0', 'hash1', 'hash2', 'entrytype',
        'title', 'author',
        'editor', 'year'], na_values=['\\N','\\',''])

    tas_df = pd.read_csv(tas_filepath, sep='\t', names=["user_id", "tag", "content_id", "content_type", "date"])

    bibtex_tas_df = tas_df[tas_df["content_type"] == 2]

    bibtex_docs_df = pd.merge(
        left=bibtex_df,
        right=(
            bibtex_tas_df.groupby("content_id")['tag'].apply(
                lambda tags: ','.join(set(tags))).to_frame().reset_index()),
        on='content_id',
        how='left'
    ).rename(
        columns={'tag': 'tags'}
    )

    return bibtex_docs_df


def load_bookmark_and_tags(bookmark_filepath, tas_filepath):
    bookmark_df = pd.read_csv(bookmark_filepath, sep='\t', error_bad_lines=False, names=[
        'content_id', 'url_hash', 'url', 'description', 'extended_description', 'date'])

    tas_df = pd.read_csv(tas_filepath, sep='\t', names=["user_id", "tag", "content_id", "content_type", "date"])

    bookmark_tas_df = tas_df[tas_df["content_type"] == 1]

    bookmark_docs_df = pd.merge(
        left=bookmark_df,
        right=(
            bookmark_tas_df.groupby("content_id")['tag'].apply(
                lambda tags: ','.join(set(tags))).to_frame().reset_index()),
        on='content_id',
        how='left'
    ).rename(
        columns={'tag': 'tags'}
    )

    return bookmark_docs_df
