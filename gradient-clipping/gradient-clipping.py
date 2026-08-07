import numpy as np

def clip_gradients(g, max_norm):
    """
    Clip gradients using global norm clipping.
    """
    # Write code here
    g = np.array(g)
    
    if np.count_nonzero(g) == 0 or max_norm <= 0:
        return g
    
    g_norm = np.sqrt(np.sum(np.square(g)))

    

    return g if g_norm <= max_norm else g*(max_norm/g_norm)