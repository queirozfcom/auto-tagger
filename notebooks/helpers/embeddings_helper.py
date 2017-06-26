import numpy as np

def build_embedding_matrix(word_index, embedding_index, max_nb_words, embedding_dim):
    """
    builds an embedding matrix, given arguments.
    
    word_index: a dict of form: (word (str) => word position (int) )
    embedding_index: a dict of form: (word (str) => embedding for that word (1-d array))
    max_nb_words: maximum number of words to consider from word_index
    embedding_dim: length of each embedding in embedding_index

    returns a matrix, with the word embedding for each word w in the word index.
    
    (if a word in word_index has no embedding in embedding_index, then a vector
    of zeros is used)
    """
    
    embedding_matrix = np.zeros((len(word_index)+1,embedding_dim))

    for word,i in word_index.items():
    
        if i >= max_nb_words:
            continue
    
        embedding_vector = embedding_index.get(word)
    
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    
    return embedding_matrix