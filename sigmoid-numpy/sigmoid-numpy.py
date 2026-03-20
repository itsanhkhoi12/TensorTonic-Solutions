import numpy as np

def sigmoid(x):
    """
    Vectorized sigmoid function.
    """
    # Write code here
    return 1/(1+np.exp(-np.asarray(x,dtype=float)))