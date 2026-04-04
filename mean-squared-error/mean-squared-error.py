import numpy as np

def mean_squared_error(y_pred, y_true):
    """
    Returns: float MSE
    """
    y_pred = np.array(y_pred)
    y_true = np.array(y_true)

    if y_pred.shape != y_true.shape:
        return None
    else:
        return np.sum(np.square(y_pred - y_true))/len(y_pred) 
