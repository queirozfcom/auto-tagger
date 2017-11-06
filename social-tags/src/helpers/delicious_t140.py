def make_path_to_file(data_root, file_hash):
    path_to_file = data_root.rstrip('/') + "/fdocuments/" + _get_directory_name_from_hash(file_hash) + "/" + file_hash + ".html"
    return path_to_file


# TODO optimize this because currently this does one I/O OP per loop
def load_contents(path_to_html_file):
    with open(path_to_html_file, "r", encoding='utf-8', errors='ignore') as f:
        contents = f.read()

    return contents


def _get_directory_name_from_hash(file_hash):
    return file_hash[:2]
