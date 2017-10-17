def make_bookmark_data(dataframe, columns=None):
    if columns is None:
        columns = ['url', 'description', 'extended_description']

    dataframe.fillna('', inplace=True)

    dataframe['contents'] = ''

    for column in columns:
        dataframe['contents'] = dataframe['contents'] + ' ' + dataframe[column]

    return dataframe["contents"].values


def make_bibtex_data(dataframe, columns=None):
    if columns is None:
        columns = ['title', 'bibtexAbstract', 'description', 'note', 'annote']

    dataframe.fillna('', inplace=True)

    dataframe['contents'] = ''

    for column in columns:
        dataframe['contents'] = dataframe['contents'] + ' ' + dataframe[column]

    return dataframe["contents"].values
