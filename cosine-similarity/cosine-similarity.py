import numpy as np

def cosine_similarity(a, b):
    """
    Compute cosine similarity between two 1D NumPy arrays.
    Returns: float in [-1, 1]
    """
    # Write code here
    a = np.array(a)
    b = np.array(b)
    euclid_norm = np.sqrt(np.sum(np.square(a))) * np.sqrt(np.sum(np.square(b)))
    if euclid_norm == 0:
        return 0.0
    else:
        return np.dot(a,b)/euclid_norm