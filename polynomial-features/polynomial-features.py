def polynomial_features(values, degree):
    """
    Generate polynomial features for each value up to the given degree.
    """
    # Write code here
    ans = []
    for value in values:
        ans.append([value**i for i in range(degree+1)])
    return ans