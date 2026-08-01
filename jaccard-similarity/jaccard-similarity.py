def jaccard_similarity(set_a, set_b):
    """
    Compute the Jaccard similarity between two item sets.
    """
    # Write code here
    set_a, set_b = set(set_a), set(set_b)
    if len(set_a) == 0 and len(set_b) == 0:
        return 0.0
        
    inter = set_a.intersection(set_b)
    uni = set_a.union(set_b)

    return len(inter) / len(uni)