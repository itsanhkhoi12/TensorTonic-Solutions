def word_count_dict(sentences):
    """
    Returns: dict[str, int] - global word frequency across all sentences
    """
    # Your code here
    words_list = []
    for sentence in sentences:
        words_list.extend(sentence)

    words_freq = dict({word:0 for word in set(words_list)})

    for word in words_list:
        if word in words_freq:
            words_freq[word]+=1

    return words_freq