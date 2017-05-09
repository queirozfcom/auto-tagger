from sklearn.feature_extraction.text import CountVectorizer

def build_inverse_word_index(word_index):
    """
    take a dict of shape word => word_index_position and return
    a dict that make the inverse transform, i.e. word_index_position => word
    """
    
    inverse_word_index = {}

    for word,i in word_index.items():
        inverse_word_index[i] = word
        
        
    return inverse_word_index