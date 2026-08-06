def popularity_ranking(items, min_votes, global_mean):
    """
    Compute the Bayesian weighted rating for each item.
    """
    # Write code here
    ranking = []
    for item in items:
        r, v = item
        wr = ((v/(v+min_votes))*r) + ((min_votes/(v+min_votes))*global_mean)
        ranking.append(wr)
    return ranking