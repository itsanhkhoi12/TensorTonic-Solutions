import numpy as np

def geometric_pmf_mean(k, p):
    """
    Compute Geometric PMF and Mean.
    """
    # Write code here
    return np.asarray((1-p)**(np.asarray(k)-1)*p),1/p