def binning(values, num_bins):
    """
    Assign each value to an equal-width bin.
    """
    # Write code here
    if len(set(values)) == 1:
        return [0] * len(values) 
    else:
        bin_values = []
        min_value = min(values)
        max_value = max(values)
        bin_width = (max_value - min_value)/num_bins
        for bin in values:
            bin = min([(bin - min_value)//bin_width, num_bins-1])
            bin_values.append(bin)
        return bin_values