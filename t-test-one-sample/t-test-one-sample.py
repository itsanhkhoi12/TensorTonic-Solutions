import numpy as np

def t_test_one_sample(x, mu0):
    """
    Compute one-sample t-statistic.
    """
    # Write code here
    x = np.asarray(x)
    n = x.shape[0]
    
    s = np.sqrt((1/(n-1))*np.sum(np.square(x-np.mean(x))))

    return (np.mean(x) - mu0)/(s/np.sqrt(n))