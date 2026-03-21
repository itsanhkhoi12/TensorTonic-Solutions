def deduplicate(records, key_columns, strategy):
    """
    Deduplicate records by key columns using the given strategy.
    """
    deduplicate_list = []
    # Write code here
    grouping_key = {}
    for record in records:
        key = tuple(record[col] for col in key_columns)
        if key not in grouping_key:
            grouping_key[key] = [record]
        else:
            grouping_key[key].append(record)
    
    for key, group_list in grouping_key.items():
        if strategy.lower() == 'first':
            deduplicate_list.append(group_list[0])
        elif strategy.lower() == 'last':
            deduplicate_list.append(group_list[-1])
        else:
            null_counts = []
            for record in group_list:
                null_count = sum([v is None for k,v in record.items()])
                null_counts.append(null_count)

            deduplicate_list.append(group_list[null_counts.index(min(null_counts))])
            

    return deduplicate_list