import numpy as np

def normalize_3d(v):
    """
    Normalize 3D vector(s) to unit length.
    """
    # Your code here
    v = np.asarray(v,dtype=float)
        
    if v.ndim == 1:
        if np.count_nonzero(v) == 0:
            return v
        else:
            return v/np.sqrt(np.sum(np.square(v)))
    else:
        norms = np.sqrt(np.sum(v**2, axis=1, keepdims=True))
        result = v.copy()
        mask = (norms.flatten() > 1e-10)
        result[mask] = v[mask] / norms[mask]
        return result        