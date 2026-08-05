def top_k_recommendations(scores, rated_indices, k):
    """
    Return indices of top-k unrated items by predicted score.
    """
    # Write code here

    unrated = [(scores[i], i) for i in range(len(scores)) if i not in rated_indices]
    unrated.sort(key=lambda x: -x[0])
    return [idx for _, idx in unrated[:k]]