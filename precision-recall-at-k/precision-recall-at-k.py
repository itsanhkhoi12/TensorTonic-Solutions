def precision_recall_at_k(recommended, relevant, k):
    """
    Compute precision@k and recall@k for a recommendation list.
    """
    # Write code here
    return [(len(set(recommended[:k]) & set(relevant))) / k, (len(set(recommended[:k]) & set(relevant))) / len(relevant)]