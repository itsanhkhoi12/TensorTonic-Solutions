def validate_records(records, schema):
    """
    Validate records against a schema definition.
    """
    # Write code here
    res = []
    for idx, record in enumerate(records):
        errors = []
        is_valid = False
        # Looping over schema
        for valid in schema:
            
            # Check missing columns
            if valid['column'] not in record:
                errors.append(f'{valid['column']}: missing')
                continue

            # Check nullable values
            if not valid['nullable'] and record[valid['column']] is None:
                errors.append(f'{valid['column']}: null')
                continue

            if valid['nullable'] and record[valid['column']] is None:
                continue

            # Check typing            
            if valid['type'] != type(record[valid['column']]).__name__:
                if valid['type'] in {'float','int'} and type(record[valid['column']]).__name__ in {'float','int'}:
                    pass
                    
                else:
                    errors.append(f'{valid['column']}: expected {valid['type']}, got {type(record[valid['column']]).__name__}')
                    continue

            # Range checking
            if valid['type'] in {'float','int'} and type(record[valid['column']]).__name__ in {'float','int'}:
                if 'min' in valid and 'max' in valid:
                    if record[valid['column']] < valid['min'] or record[valid['column']] > valid['max']:
                        errors.append(f'{valid['column']}: out of range')
                        continue

                 
        if len(errors) == 0:
            is_valid = True
        res.append((idx,is_valid,errors))

    return res
        