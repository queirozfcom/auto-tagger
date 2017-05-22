import numpy as np

  
def get_tag_assignment(strategy,predicted_tag_probabilities,**kwargs):
    """
    Takes as parameter a strategy and a numpy ndarray containing N tag probabilities,
    such as those output by a neural net with N output units.
    
    Additionaly, extra keyword arguments are required for the chosen strategy. E.g.,     strategy "static_threshold" requires a keyword argument named "threshold" to be
    provided.
    
    All strategies support a "limit" argument. The default behaviour is to return
    all tags that meet the criteria.
    
    Returns a binary tag assignment array, converting tag probabilities into actual
    tag assignments, according to the chosen strategy.
    
    """
    
    supported_strategies = [
        "raw_probability",
        "absolute_difference_wrt_tag_incidence",
        "relative_difference_wrt_tag_incidence",
        "absolute_difference_wrt_estimated_tag_probability",
        "relative_difference_wrt_estimated_tag_probability"
    ]
    
    clean_strat = strategy.lower().strip()
    
    if clean_strat not in supported_strategies:
        raise Exception("provided strategy does not match supported strategies")
    
    if kwargs is None:
        raise Exception("no strategy-specific kw arguments provided")
    
    maybe_limit = kwargs.get("limit")
    
    if clean_strat == "raw_probability":
        
        maybe_threshold = kwargs.get("probability_threshold")
        
        if maybe_threshold is None:
            raise Exception("keyword argument \"probability_threshold\" must be provided for strategy=\"raw_probability\"")
        
        return _get_by_raw_probability(predicted_tag_probabilities,
                                 maybe_threshold,
                                 maybe_limit)

    
    elif clean_strat == "absolute_difference_wrt_tag_incidence":
        maybe_tag_incidence_index = kwargs.get("tag_incidence_index")
        
        if maybe_tag_incidence_index is None:
            raise Exception("keyword argument \"tag_incidence_index\" must be provided for strategy=\"absolute_difference_wrt_tag_incidence\"")
        
        return _get_by_difference_wrt_tag_incidence(
                                        predicted_tag_probabilities,
                                        maybe_limit,
                                        maybe_tag_incidence_index,
                                        True)
    
    
    elif clean_strat == "relative_difference_wrt_tag_incidence":
        maybe_tag_incidence_index = kwargs.get("tag_incidence_index")
        
        if maybe_tag_incidence_index is None:
            raise Exception("keyword argument \"tag_incidence_index\" must be provided for strategy=\"relative_difference_wrt_tag_incidence\"")
        
        return _get_by_difference_wrt_tag_incidence(
                                        predicted_tag_probabilities,
                                        maybe_limit,
                                        maybe_tag_incidence_index,
                                        False)
    
    
    elif clean_strat == "absolute_difference_wrt_estimated_tag_probability":
        maybe_tag_prob_index = kwargs.get("tag_probability_index")   
    
        if maybe_tag_prob_index is None:
            raise Exception("keyword argument \"tag_probability_index\" must be provided for strategy=\"absolute_difference_wrt_estimated_tag_probability\"")
            
        return _get_by_difference_wrt_tag_estimated_probability(
                                   predicted_tag_probabilities,
                                   maybe_limit,
                                   maybe_tag_prob_index,
                                   True)
        
    elif clean_strat == "relative_difference_wrt_estimated_tag_probability":
        maybe_tag_prob_index = kwargs.get("tag_probability_index")   
    
        if maybe_tag_prob_index is None:
            raise Exception("keyword argument \"tag_probability_index\" must be provided for strategy=\"relative_difference_wrt_estimated_tag_probability\"")
            
        return _get_by_difference_wrt_tag_estimated_probability(
                                   predicted_tag_probabilities,
                                   maybe_limit,
                                   maybe_tag_prob_index,
                                   False)
        
    else:
        raise Exception("unsupported strategy: {}".format(clean_strat))        
                                        

def truncate_labels(labels,min_doc_count):
    """
    labels is an array of label sets.
    
    remove labels that occur in less than min_doc_count documents
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
            

def get_incidence_index(Y_train):
    """
    Takes as argument a NxM ndarray, where N is the number of training
    cases and M is the number of possible tags. 
    
    returns a dictionary mapping tag indices to floats, where the float 
    is the fraction of samples having that tag in the dataset.
    
    Note: using the full (train+set) data to obtain this characterizes snooping, if
    used for inference.
    """
    
    index = dict()
    
    for i,value in enumerate(np.mean(Y_train,axis=0)):
        index[i] = value
    
    return index

def get_probability_index(Y_train_pred):
    """
    Takes as argument a NxM ndarray, where N is the number of training
    cases and M is the number of possible tags. 
    
    Each row of this matrix is the output of a multi-output neural network,
    for multi-label classification.
    
    Returns a dict (tag_position => average_probability), that relates each tag
    to the average probability (over all traiing cases) the predictive model has
    assigned to that label.
    
    Note: using the full (train+set) data to obtain this characterizes snooping, if
    used for inference.
    """   
    
    index = dict()
    
    for i,value in enumerate(np.mean(Y_train_pred,axis=0)):
        index[i] = value
    
    return index    
    
###############################################    
## PRIVATE   
###############################################

def _get_by_raw_probability(predicted_tag_probabilities,
                      threshold,
                      limit):
    """
    converts a tag probability array into a binary tag assignment array, according
    to this strategy.
    """
     
    tags_and_probs = [ (tag_pos,prob) for tag_pos,prob in enumerate(predicted_tag_probabilities.ravel()) if prob > threshold ]
   
    sorted_tags_probs = sorted(tags_and_probs,key=lambda tpl:tpl[1],reverse=True)
    
    if limit is None:
        tags_ordered = [tag for tag,_ in sorted_tags_probs]
    else:    
        tags_ordered = [tag for tag,_ in sorted_tags_probs][:limit]
    
    predicted_label_indices = np.zeros(len(predicted_tag_probabilities),dtype='int64')
       
    predicted_label_indices[tags_ordered] = 1   
          
    return predicted_label_indices.reshape(1,-1)  
    
    
def _get_by_difference_wrt_tag_incidence(
    predicted_tag_probabilities,
    limit,
    tag_incidence_index,
    use_absolute_difference):
    """
    converts a tag probability array into a binary tag assignment array, according
    to this strategy.
    
    tag_incidence_index is a dictionary whose keys are tag positions and values
    are the percentage of documents that have that tag in the training set.
    
    (if predicted_index is not in the index, assume the average over all tags)
    """ 
    
    # global_mean is used for cases when predicted tag is not in the provided
    # index. This can happen for tags that showed up in the test set
    # but not in the training set.
    #
    # this can be put outside to save time
    global_sum = sum([value for _,value in tag_incidence_index.items()])
    global_mean = global_sum / len(tag_incidence_index)
    
    if use_absolute_difference:
        tag_positions_and_diffs = [__get_absolute_score_wrt_tag_incidence(tag_pos,proba,tag_incidence_index, global_mean) for tag_pos,proba in enumerate(predicted_tag_probabilities.ravel())]
    else:
        tag_positions_and_diffs = [__get_relative_score_wrt_tag_incidence(tag_pos,proba,tag_incidence_index,global_mean) for tag_pos,proba in enumerate(predicted_tag_probabilities.ravel())]
          
    sorted_tags_by_diffs = sorted(tag_positions_and_diffs,key=lambda tpl:tpl[1],reverse=True)
    
    if limit is None:
        tags_ordered = [tag for tag,_ in sorted_tags_by_diffs]
    else:    
        tags_ordered = [tag for tag,_ in sorted_tags_by_diffs][:limit]
    
    predicted_label_indices = np.zeros(len(predicted_tag_probabilities),dtype='int64')
       
    predicted_label_indices[tags_ordered] = 1   
          
    return predicted_label_indices.reshape(1,-1)     

def _get_by_difference_wrt_tag_estimated_probability(
                                   predicted_tag_probabilities,
                                   limit,
                                   tag_probability_index,
                                   use_absolute_difference):
    """
    converts a tag probability array into a binary tag assignment array, according
    to this strategy.
    
    tag_probability_index is a dictionary whose keys are tag positions and values
    are the average score for each tag in by the trained model.
    
    (if predicted_index is not in the index, assume the average over all tags)
    """ 
    
    # global_mean is used for cases when predicted tag is not in the provided
    # index. This can happen for tags that showed up in the test set
    # but not in the training set.
    #
    # this can be put outside to save time
    global_sum = sum([value for _,value in tag_probability_index.items()])
    global_mean = global_sum / len(tag_probability_index)
    
    if use_absolute_difference:
        scoring_func = __get_absolute_score_wrt_estimated_tag_probability
    else:
        scoring_func = __get_relative_score_wrt_estimated_tag_probability
    
    tag_positions_and_diffs = [ scoring_func(tag_pos,proba,tag_probability_index,global_mean) for tag_pos,proba in enumerate(predicted_tag_probabilities.ravel())]
   
    sorted_tags_by_diffs = sorted(tag_positions_and_diffs,key=lambda tpl:tpl[1],reverse=True)
    
    if limit is None:
        tags_ordered = [tag for tag,_ in sorted_tags_by_diffs]
    else:    
        tags_ordered = [tag for tag,_ in sorted_tags_by_diffs][:limit]
    
    predicted_label_indices = np.zeros(len(predicted_tag_probabilities),dtype='int64')
       
    predicted_label_indices[tags_ordered] = 1   
          
    return predicted_label_indices.reshape(1,-1)
    
###############################################    
## HELPERS   
###############################################    


    
def __get_absolute_score_wrt_tag_incidence(tag_pos, 
                                          predicted_tag_proba,
                                          tag_incidence_index,
                                          global_mean):
       
    incidence_for_this_tag = tag_incidence_index.get(tag_pos)
    
    if incidence_for_this_tag is None or incidence_for_this_tag == 0:
        return (tag_pos, predicted_tag_proba - global_mean)
    else:
        return (tag_pos, predicted_tag_proba - incidence_for_this_tag) 

def __get_relative_score_wrt_tag_incidence(tag_pos, 
                                          predicted_tag_proba,
                                          tag_incidence_index,
                                          global_mean):
       
    incidence_for_this_tag = tag_incidence_index.get(tag_pos)
    
    if incidence_for_this_tag is None or incidence_for_this_tag == 0:
        return (tag_pos, (predicted_tag_proba - global_mean)/global_mean)
    else:
        return (tag_pos, (predicted_tag_proba - incidence_for_this_tag) / incidence_for_this_tag)

    
def __get_absolute_score_wrt_estimated_tag_probability(tag_pos, 
                                          predicted_tag_proba,
                                          tag_probability_index,
                                          global_mean):
    
    estimated_probability_for_this_tag = tag_probability_index.get(tag_pos)
    
    if estimated_probability_for_this_tag is None or estimated_probability_for_this_tag == 0:
        return (tag_pos, predicted_tag_proba - global_mean)
    else:
        return (tag_pos, predicted_tag_proba - estimated_probability_for_this_tag)     
    
    
def __get_relative_score_wrt_estimated_tag_probability(tag_pos, 
                                          predicted_tag_proba,
                                          tag_probability_index,
                                          global_mean):
       
    estimated_probability_for_this_tag = tag_probability_index.get(tag_pos)
    
    if estimated_probability_for_this_tag is None or estimated_probability_for_this_tag == 0:
        return (tag_pos, (predicted_tag_proba - global_mean)/global_mean)
    else:
        return (tag_pos, (predicted_tag_proba - estimated_probability_for_this_tag) / estimated_probability_for_this_tag)    
    
    

        
    
def deprecated_truncate_binary_labels(Y_train,min_doc_count):
    """
    remove tags that occur in less than min_doc_count documents
    
    Y_train is an NxM ndarray, each row being a N-hot-encoded binary array,
    indicating what labels are active for that sample.
    
    Returns a truncated version of Y_train with some columns removed - columns
    that refer to labels that appear in less than min_doc_count rows.
    """
    
    doc_counts = np.sum(Y_train,axis=0)
    
    good_tag_indices = np.where(doc_counts >= min_doc_count)
    
    new_Y_train = Y_train.T[good_tag_indices].T
    
    assert Y_train.shape[0] == new_Y_train.shape[0]
    
    return new_Y_train    
    
    
  