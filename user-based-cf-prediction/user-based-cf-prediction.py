def user_based_cf_prediction(similarities, ratings):
    """
    Predict a rating using user-based collaborative filtering.
    """
    # Write code here
    if all(similarity <= 0 for similarity in similarities):
        return 0.0

    deno, nume = 0, 0
    
    for i in range(len(similarities)):
        if similarities[i] <= 0:
            continue
        else:
            deno = deno + similarities[i] * ratings[i]
            nume += similarities[i]

    return deno/nume