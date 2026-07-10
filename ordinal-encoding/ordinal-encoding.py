def ordinal_encoding(values, ordering):
    """
    Encode categorical values using the provided ordering.
    """
    # Write code here

    encoding_map = dict(zip(ordering,range(len(ordering))))
    res = []

    for val in values:
        res.append(encoding_map[val])

    return res