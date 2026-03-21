def robust_scaling(values):
    """
    Scale sorted_values using median and interquartile range.
    """
    # Write code here
    if len(values) < 2:
        return [0.0]
    else:
        sorted_values = sorted(values)
    
        def _get_median_value(values):
            if len(values)%2!=0:
                median_value = values[len(values)//2]
            else:
                median_value = (values[len(values)//2] + values[((len(values)//2))-1]) / 2
            return median_value
    
        median_value = _get_median_value(sorted_values)

        if len(sorted_values)%2!=0:
            lower_half = sorted_values[:len(sorted_values)//2]
            upper_half = sorted_values[(len(sorted_values)//2)+1:]
            q1 = _get_median_value(lower_half)
            q3 = _get_median_value(upper_half)

        else:
            lower_half = sorted_values[:len(sorted_values)//2]
            upper_half = sorted_values[(len(sorted_values)//2):]
            q1 = _get_median_value(lower_half)
            q3 = _get_median_value(upper_half)

        iqr = q3-q1

        if iqr == 0:
            return list(map(lambda x: x - median_value, values))    
        else:
            return list(map(lambda x: (x - median_value)/iqr, values))