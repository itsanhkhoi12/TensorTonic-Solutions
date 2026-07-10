def percent_change(series):
    """
    Compute the fractional change between consecutive values.
    """
    # Write code here
    perc = []
    for i in range(1,len(series)):
        if series[i-1] == 0.0:
            perc.append(0.0)
        else:
            perc.append((series[i] - series[i-1]) / series[i-1])
    return perc