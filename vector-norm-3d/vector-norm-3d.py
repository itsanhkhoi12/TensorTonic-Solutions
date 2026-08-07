import numpy as np

def vector_norm_3d(v):
    """
    Compute the Euclidean norm of 3D vector(s).
    """
    # Your code here
    v = np.asarray(v,dtype=float)
    
    if v.ndim == 1:
        return np.sqrt(np.sum(np.square(v)))
    else:
        return np.sqrt(np.sum(np.square(v),axis=1))
