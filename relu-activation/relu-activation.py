import numpy as np

def relu(x):
    """
    Implement ReLU activation function.
    """
    # Write code here
    return np.maximum(0,np.array(x))