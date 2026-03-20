import numpy as np

def pad_sequences(seqs, pad_value=0, max_len=None):
    """
    Returns: np.ndarray of shape (N, L) where:
      N = len(seqs)
      L = max_len if provided else max(len(seq) for seq in seqs) or 0
    """
    # Your code here
    pad_seqs = []
    if max_len is None:
        max_len = max(list(map(lambda x: len(x),seqs)))
    
    for seq in seqs:
        if len(seq) < max_len:
            seq = np.concatenate([np.array(seq), np.full(max_len-len(seq),pad_value)])
            pad_seqs.append(seq)
        elif len(seq) > max_len:
            seq = np.array(seq)[:max_len]
            pad_seqs.append(seq)
        else:
            pad_seqs.append(seq)
    return np.array(pad_seqs)