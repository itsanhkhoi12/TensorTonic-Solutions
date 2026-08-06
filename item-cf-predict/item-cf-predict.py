def item_cf_predict(user_ratings, item_similarities, target):
    """
    Predict the rating using item-based collaborative filtering.
    """
    # Write code here
    if all(similarity <= 0 for similarity in item_similarities):
        return 0.0

    else:
        sum_rating, sum_similarities = 0,0
        for i in range(len(user_ratings)):
            if i == target or user_ratings[i] == 0 or item_similarities[i]<0:
                continue
                
            sum_rating+= (user_ratings[i]*item_similarities[i])
            sum_similarities+=item_similarities[i]

    return sum_rating/sum_similarities