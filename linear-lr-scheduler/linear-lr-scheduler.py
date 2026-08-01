def linear_lr(step, total_steps, initial_lr, final_lr=0.0, warmup_steps=0) -> float:
    """
    Linear warmup (0→initial_lr) then linear decay (initial_lr→final_lr).
    Steps are 0-based; clamp at final_lr after total_steps.
    """
    # Write code here
    if warmup_steps == 0 and step < 0:
        return 0.0
    else:
        if step >= total_steps:
            return final_lr
        if step < warmup_steps:
            return (step*initial_lr)/warmup_steps
        if warmup_steps<= step <= total_steps:
            return final_lr + ((initial_lr - final_lr) * ((total_steps-step)/(total_steps-warmup_steps)))
            