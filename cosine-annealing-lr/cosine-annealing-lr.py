import math

def cosine_annealing_schedule(base_lr, min_lr, total_steps, current_step):
    """
    Compute the learning rate using cosine annealing.
    """
    # Write code here
    if current_step == 0:
        return base_lr
    if current_step == total_steps:
        return min_lr
    else:
        return min_lr + (0.5*(base_lr-min_lr)*(1+math.cos((math.pi*current_step)/total_steps)))