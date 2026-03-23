import numpy as np

def tanh(x):
    """
    Implement Tanh activation function.
    """
    # Write code here
    x = np.asarray(x,float)
    return (np.exp(x) - np.exp(-x))/(np.exp(x) + np.exp(-x))