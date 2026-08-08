def moving_median(values, window_size):
    """
    Compute the rolling median for each window position.
    """
    # Write code here
    i = 0
    meds = []
    while i+window_size <= len(values):
        window = sorted(values[i:i+window_size])
        if window_size%2 != 0:
            med = window[window_size//2]
            meds.append(med)
        else:
            med = (window[window_size//2]+window[(window_size//2)-1] )/ 2.0
            meds.append(med)
        i+=1
    return meds