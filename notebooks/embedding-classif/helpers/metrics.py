from sklearn import metrics
import numpy as np

def calculate_multilabel_metrics(
    model, 
    X_test, 
    Y_test,
    metric='f1',
    threshold=0.10):
    """
    model is a keras model
    X_test is a matrix of shape (num_samples, num_features)
    Y_test is a one-hot matrix of shape (num_samples, num_labels)
    """
    
    if metric not in ['f1','precision','recall']:
        raise Exception("metric must be one of: 'f1','precision','recall'")
    
    Y_pred_lst = []

    for x_test in X_test:
        predicted_label_indices = np.zeros(Y_test.shape[1]).reshape(1,-1)
        bool_vec = model.predict(x_test.reshape(1,-1)) > threshold
        predicted_label_indices[bool_vec] = 1

        Y_pred_lst.append(predicted_label_indices)
    
    Y_pred = np.vstack(Y_pred_lst)
    
    if metric == 'f1':    
        return metrics.f1_score(Y_test,Y_pred, average='micro')
    elif metric == 'precision':
        return metrics.precision_score(Y_test,Y_pred, average='micro')
    elif metric =='recall':
        return metrics.recall_score(Y_test,Y_pred, average='micro')