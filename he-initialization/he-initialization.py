import math

def he_initialization(W, fan_in):
    """
    Scale raw weights to He uniform initialization.
    """
    # Write code here
    limit = math.sqrt(6/fan_in) 
    scaled_matrix = []
    for row in W:
        scaled_row = []
        for element in row:
            scaled_row.append(element*2*limit - limit)
        scaled_matrix.append(scaled_row)

    return scaled_matrix