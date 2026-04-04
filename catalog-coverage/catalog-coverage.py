def catalog_coverage(recommendations, n_items):
    """
    Compute the catalog coverage of a recommender system.
    """
    # Write code here
    items = []
    for recommendation in recommendations:
        items.extend(recommendation)
        
    if len(items) == 0:
        return 0

    return len(set(items))/n_items