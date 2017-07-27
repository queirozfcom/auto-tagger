import numpy as np

from difflib import SequenceMatcher,get_close_matches
from scipy import spatial

def get_metrics_for_tag_pair(tag_a, 
                      tag_b, 
                      tag_vectors_index, 
                      pairwise_similarity_index,
                      global_similarity_index):
    """
    given two tags a and b, returns the difference between the global similarity with respect to 
    tag a and tag b, and the mutual similarity between tag a and tag b.
    
    arguments:
        tag_a: string
        tag_b: string
        tag_vectors_index: dict: "tag_name" => numpy_array_that_represents tag_name
        pairwise_similarity_index: dict: "tag_name" => list of tuples of the form ("other_tag_name", similarity_between_tag_name_and_other_tag_name)
        global_similarity_index: dict: "tag_name" => average similarity of all other tags with tag_name
    
    returns:
        tuple: (difference_of_global_averages, mutual_similarity)
    """
                   
    avg_sim_wrt_tag_a = global_similarity_index[tag_a]
    avg_sim_wrt_tag_b = global_similarity_index[tag_b]
    
    try:
        vec_a = tag_vectors_index[tag_a]
    except KeyError:
        print("{} is not a valid tag. These are: {}".format(tag_a,_get_similar_sounding_tags(tag_a)))
        return

    try:
        vec_b = tag_vectors_index[tag_b]
    except KeyError:
        print("{} is not a valid tag. These are: {}".format(tag_b,_get_similar_sounding_tags(tag_b))) 
        return
    
    mutual_sim = _cosine_similarity(vec_a,vec_b)
        
    return (avg_sim_wrt_tag_a-avg_sim_wrt_tag_b,mutual_sim)

def get_top_k_most_similar_tags(index, target_tag_name, k):  
    """
    
    returns top most similar tags, according to cosine similarity
    
    arguments:
        index is a dict tag_name => tag_vector
        target_tag_name is a string
        k is an int
        
    returns:
        a list, with the K tags most similar to `target_tag_name`
    """
    
    target_tag_vector = index[target_tag_name]

    # calculating the similarites
    similarities = list()
    curr_best = np.NINF
    curr_tag = None

    for (tag_name,tag_vector) in index.items():
        
        if np.array_equal(tag_vector,target_tag_vector):
            continue
        
        sim = _cosine_similarity(target_tag_vector,tag_vector)
            
        similarities.append((tag_name,sim))

        if sim > curr_best and tag_name != target_tag_name:
            curr_best = sim
            curr_tag = tag_name

    sorted_similarities = sorted(similarities,key=lambda t: t[1],reverse=True)
    
    return sorted_similarities[:k]

def _get_similar_sounding_tags(tag,tag_vocabulary):
    return get_close_matches(tag,tag_vocabulary)

def _cosine_similarity(a,b):
    return 1 - spatial.distance.cosine(a, b)