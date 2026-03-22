import numpy as np

def expected_value_discrete(x, p):
    """
    Returns: float expected value
    """
    # Write code here
    if np.sum(p) != 1:
        raise ValueError
    else:
        return np.sum(np.dot(x,p))
    
