def rank_transform(values):
    """
    Replace each value with its average rank.
    """
    # Write code here
    sorted_values = sorted(values)
    freq_dict = {}
    ranking_values = {}
    for rank, value in enumerate(sorted_values,1):
        if value not in freq_dict:
            freq_dict[value] = [rank]
        else:
            freq_dict[value].append(rank)
    
    for value, rank_list in freq_dict.items():
        if len(rank_list) >= 2:
            ranking_values[value] = sum(rank_list)/len(rank_list)
        else:
            ranking_values[value] = rank_list[0]
    
    return list(map(lambda x:ranking_values[x],values))