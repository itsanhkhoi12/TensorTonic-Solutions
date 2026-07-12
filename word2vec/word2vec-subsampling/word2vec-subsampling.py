import torch

def subsample_keep_probs(counts: torch.Tensor, t: float = 1e-5) -> torch.Tensor:
    """
    Returns torch.Tensor of shape (vocab_size,) with the keep-probability for each word.
    """
    # YOUR CODE HERE

    total_counts = torch.sum(counts)
    freq = counts/total_counts
    prob_keep = torch.sqrt(t/freq)

    return torch.clamp(prob_keep,max=1.0)
    