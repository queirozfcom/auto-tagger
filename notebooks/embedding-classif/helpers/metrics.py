from sklearn import metrics
import numpy as np

def calculate_multilabel_metrics(
    Y_test, 
    Y_pred,
    metric='f1'):
    """
    Y_test is a n-hot matrix of shape (num_samples, num_labels)
    Y_pred is a n-hot matrix of shape (num_samples, num_labels)
    """
    
    if metric not in ['f1','precision','recall']:
        raise Exception("metric must be one of: 'f1','precision','recall'")
       
    if metric == 'f1':    
        return metrics.f1_score(Y_test,Y_pred, average='micro')
    elif metric == 'precision':
        return metrics.precision_score(Y_test,Y_pred, average='micro')
    elif metric =='recall':
        return metrics.recall_score(Y_test,Y_pred, average='micro')