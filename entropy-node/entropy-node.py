import numpy as np

def entropy_node(y):
    """
    Compute entropy for a single node using stable logarithms.
    """
    # Write code here
    n = len(y)
    y = np.asarray(y,dtype = int)
    
    if n == 0:
        return 0.0

    _, counts = np.unique(y, return_counts = True)

    probs = counts / len(y)
    probs = probs[probs > 0]

    return -np.sum(probs*np.log2(probs))