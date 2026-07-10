def validate_records(records, schema):
    NUMERIC_TYPES = {"int", "float"}
    results = []

    for idx, record in enumerate(records):
        errors = []

        for rule in schema:
            column = rule["column"]
            expected_type = rule["type"]
            nullable = rule["nullable"]

            if column not in record:
                errors.append(f"{column}: missing")
                continue

            value = record[column]

            if value is None:
                if not nullable:
                    errors.append(f"{column}: null")
                continue

            actual_type = type(value).__name__

            if expected_type != actual_type:
                if not (
                    expected_type in NUMERIC_TYPES
                    and actual_type in NUMERIC_TYPES
                ):
                    errors.append(
                        f"{column}: expected {expected_type}, got {actual_type}"
                    )
                    continue

            if expected_type in NUMERIC_TYPES:
                if "min" in rule and value < rule["min"]:
                    errors.append(f"{column}: out of range")
                    continue

                if "max" in rule and value > rule["max"]:
                    errors.append(f"{column}: out of range")

        results.append((idx, not errors, errors))

    return results