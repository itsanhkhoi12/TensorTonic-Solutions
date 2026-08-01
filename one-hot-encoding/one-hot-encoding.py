import numpy as np

def one_hot(y, num_classes=None):
    """
    Convert integer labels y ∈ {0,...,K-1} into one-hot matrix of shape (N, K).
    """
    # Write code here
    max_class = num_classes if num_classes else max(y)+1
    ohe_output = np.array([np.zeros(max_class)] * len(y))
    for i,feature in enumerate(y):
        ohe_output[i,feature] = 1

    return ohe_output
        