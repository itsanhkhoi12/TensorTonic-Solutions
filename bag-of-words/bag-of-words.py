import numpy as np

def bag_of_words_vector(tokens, vocab):
    """
    Returns: np.ndarray of shape (len(vocab),), dtype=int
    """
    # Your code here
    vocab_frequency = dict({token: 0 for token in vocab})
    for token in tokens:
        if token in vocab:
            vocab_frequency[token] += 1

    return np.asarray(list(vocab_frequency.values()),dtype = int)
