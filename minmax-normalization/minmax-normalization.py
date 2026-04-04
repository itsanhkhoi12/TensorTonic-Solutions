import numpy as np

def minmax_scale(X, axis=0, eps=1e-12):
    """
    Scale X to [0,1]. If 2D and axis=0 (default), scale per column.
    Return np.ndarray (float).
    """
    # Write code here
    X = np.array(X)
    X_min = np.min(X,axis = axis, keepdims=True)
    X_max = np.max(X, axis = axis, keepdims=True)
    diff = X_max - X_min
    deno = np.where(diff == 0, diff+eps,diff)
    
    return (X - X_min)/deno
