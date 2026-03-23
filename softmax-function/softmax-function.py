import numpy as np

def softmax(x):
    """
    Compute the softmax of input x.
    Works for 1D or 2D NumPy arrays.
    For 2D, compute row-wise softmax.
    """
    # Write code here
    x = np.array(x)
    max_value = np.max(x,axis=-1,keepdims=True)
    e_x = np.exp(x-max_value)
    soft_max_sum = np.sum(e_x,axis = -1, keepdims = True)
    return e_x/soft_max_sum