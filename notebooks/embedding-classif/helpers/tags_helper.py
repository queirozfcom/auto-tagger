import numpy as np

  
    

def get_probabilities_index(Y):
    """
    Y is a np.ndarray, where each row is a n-hot vector
    
    returns a dictionary mapping tag indices to floats,
    where the float is the fraction of samples
    having that tag in the dataset
    """
    
    counts_index = dict()
    
    for row in Y:
        indices = row.nonzero()[0]
               
        for i in indices:
            if counts_index.get(i) is None:
                counts_index[i] = 1
            else:    
                counts_index[i] = counts_index[i] + 1
    
    
    num_tags = len(counts_index)
    
    proportion_index = dict()
    
    for idx,value in counts_index.items():
        proportion_index[idx] = value / num_tags / 100
            
    return proportion_index
    
def get_predicted_indices_by_threshold(predicted_tag_probabilities,
                                   threshold=0.08):
    
    predicted_label_indices= np.zeros(len(predicted_tag_probabilities),dtype='int64')
    
    predicted_label_indices[predicted_tag_probabilities > threshold] = 1

    return predicted_label_indices
    
    
def get_predicted_indices_by_tag_doc_fraction(
    tag_probabilities_index,
    predicted_tag_probabilities,
    relative_difference_threshold=None):
    """
    
    (if predicted_index is not in the index, assume the average over all tags
    """
       
    output = []

    # this can be put outside to save time
    sum_over_all_tags = sum([value for _,value in tag_probabilities_index.items()])

    # no need for float casting in python 3
    mean_over_all_tags = sum_over_all_tags / len(tag_probabilities_index)

    for i,prob in enumerate(predicted_tag_probabilities.ravel()):

        avg_prob = tag_probabilities_index.get(i)
        
        relative_difference = (prob-avg_prob)/avg_prob
        
        if avg_prob is None or relative_difference_threshold is None:
            if prob > mean_over_all_tags:
                output.append(1)
            else:
                output.append(0)
        else:
            if prob > avg_prob and relative_difference > relative_difference_threshold:
                output.append(1)
            else:
                output.append(0)

    return np.array(output).reshape(1,-1)
    
    
def get_top_k_predicted_indices(
    predicted_tag_probabilities,
    k=5):
    """
    
    (if predicted_index is not in the index, assume the average over all tags
    """
    
    
    tags_probs = [ (tag,prob) for tag,prob in enumerate(predicted_tag_probabilities.ravel())]
   
    sorted_tags_probs = sorted(tags_probs,key=lambda tpl:tpl[1],reverse=True)
       
    tags_ordered = [tag for tag,_ in sorted_tags_probs][:k]
    
    predicted_label_indices = np.zeros(len(tags_probs),dtype='int64')
       
    predicted_label_indices[tags_ordered] = 1   
       
    predicted_label_indices = predicted_label_indices.reshape(1,-1)
    
    return predicted_label_indices
   

    
def truncate_labels(labels,min_doc_count):
    """
    $labels is an array of arrays of strings
    
    remove tags that occur in less than $min_doc_count
    documents
    """
    
    label_index = dict()
    
    for label_row in labels:
        
        for label in label_row:
            if label_index.get(label) is None:
                label_index[label] = 1
            else:
                label_index[label] = label_index[label] + 1
                
    good_labels = []
    
    for label,doc_count in label_index.items():
        if doc_count >= min_doc_count:
            good_labels.append(label)
            
     
    new_labels = []
        
    for label_row in labels:
        new_labels.append([label for label in label_row if label in good_labels])
        
    return new_labels   
    
    
def truncate_binary_labels(Y_train,min_doc_count):
    """
    remove tags that occur in less than $min_doc_count
    documents
    """
    
    doc_counts = np.sum(Y_train,axis=0)
    
    good_tag_indices = np.where(doc_counts >= min_doc_count)
    
    new_Y_train = Y_train.T[good_tag_indices].T
    
    assert Y_train.shape[0] == new_Y_train.shape[0]
    
    return new_Y_train    
    
    
  