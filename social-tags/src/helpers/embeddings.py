import os
import numpy as np


def read_glove_wiki_weighted(d, weight_index, glove_dir = None):

    if glove_dir is None:
        glove_dir = "/media/felipe/SAMSUNG/GloVe"

    supported_dimensions = [50, 100, 200, 300]

    if d not in supported_dimensions:
        raise ValueError("argument d must be one of {0}".format(",".join(supported_dimensions)))


    embeddings_index = {}

    matches = 0
    overall = 0

    with open(os.path.join(glove_dir, "glove.6B.{0}d.txt".format(d)), 'r') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')

            maybe_weight = weight_index.get(word)

            if maybe_weight is None:
                weight = 1.0
            else:
                weight = maybe_weight
                matches += 1

            overall += 1
            embeddings_index[word] = coefs * weight

    print("overall, {0} out of {1} embeddings were weighted. Total available embeddings: {2}".format(matches,
                                                                                                     len(weight_index),
                                                                                                     overall))

    return embeddings_index
