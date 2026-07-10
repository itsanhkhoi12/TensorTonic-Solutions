def seasonal_average(series, period):
    """
    Compute the average value for each position in the seasonal cycle.
    """
    # Write code here
    avg_vals = [0] * period
    for i in range(len(avg_vals)):
        avg_vals[i] = sum(series[i:len(series):period])/len(series[i:len(series):period])

    return avg_vals