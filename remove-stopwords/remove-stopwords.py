def remove_stopwords(tokens, stopwords):
    """
    Returns: list[str] - tokens with stopwords removed (preserve order)
    """
    # Your code here
    output_token = []
    for token in tokens:
        if token not in stopwords:
            output_token.append(token)
    return output_token