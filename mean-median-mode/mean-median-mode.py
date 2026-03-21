import numpy as np
from collections import Counter

def mean_median_mode(x):
    """
    Compute mean, median, and mode.
    """
    # Write code here
    x = np.array(x)
    # If an array has only an single element, return mean = median = mode = that single element
    if len(x) < 2:
        return (x[0],x[0],x[0])
    else:
        mean = np.mean(x)
        median = np.median(x)
        most_freq_elements = [key for key,val in Counter(x).items() if val == max(Counter(x).values())]
        mode = min(most_freq_elements)
        return (mean, median, mode)
    