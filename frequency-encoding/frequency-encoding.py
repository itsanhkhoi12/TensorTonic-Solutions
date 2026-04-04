def frequency_encoding(values):
    """
    Replace each value with its frequency proportion.
    """
    # Write code here
    total_values = len(values)
    freq = dict({k:0 for k in set(values)})
    for value in values:
        freq[value]+=1
    return list(map(lambda x: freq[x]/total_values, values))