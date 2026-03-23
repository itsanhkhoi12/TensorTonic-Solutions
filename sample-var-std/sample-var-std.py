import numpy as np

def sample_var_std(x):
    """
    Compute sample variance and standard deviation.
    """
    # Write code here
    x = np.array(x)
    var = (1/(len(x)-1))*(np.sum(np.square(x-np.mean(x))))
    std = np.sqrt(var)
    return (var,std)