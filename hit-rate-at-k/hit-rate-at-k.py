def hit_rate_at_k(recommendations, ground_truth, k):
    """
    Compute the hit rate at K.
    """
    # Write code here
    hit_rate = 0
    for ground_truth, recommendation in zip(ground_truth, recommendations):
        for point in recommendation[:k]:
            if point in ground_truth:
                hit_rate+=1
                
    return hit_rate/len(recommendations)