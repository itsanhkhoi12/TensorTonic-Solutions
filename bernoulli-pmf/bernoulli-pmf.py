import numpy as np

def bernoulli_pmf_and_moments(x, p):
    """
    Compute Bernoulli PMF and distribution moments.
    """
    # Write code here
    pmf = np.where(np.array(x)==1,p,1-p)
    mean = p
    var = p*(1-p)
    return (pmf,mean,var)