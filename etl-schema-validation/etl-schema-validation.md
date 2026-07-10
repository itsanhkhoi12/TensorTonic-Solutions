## The Problem: Bad Data Silently Corrupts Everything Downstream

In data pipelines, raw data arrives from many sources: user events, API responses, third-party feeds, IoT sensors, and manual uploads. This data is often messy, inconsistent, or outright wrong. If you load it directly into your data warehouse without validation, the problems propagate to every downstream consumer: dashboards show wrong numbers, ML models train on corrupted features, and business decisions are made on faulty information.

The insidious aspect of data quality issues is that they often go unnoticed for a long time. A missing field defaults to null, an incorrect type gets coerced, an out-of-range value looks plausible at first glance. By the time someone notices the problem, months of data may be corrupted, and tracking down the root cause becomes a nightmare.

**Schema validation** is the first line of defense. Before loading any record into the warehouse, you validate it against a schema that defines what columns should exist, what types they should have, whether nulls are allowed, and what value ranges are acceptable. Invalid records are flagged and routed to a dead-letter queue for investigation, while valid records proceed to the warehouse.

---

## What is a Schema?

A **schema** defines the expected structure and constraints of your data. For tabular data, a schema specifies for each column:

**Column Name**: The identifier for this field

**Data Type**: What kind of value is expected (integer, float, string, etc.)

**Nullable**: Whether the field can be absent or contain null values

**Range Constraints**: For numeric fields, minimum and maximum acceptable values

A well-designed schema acts as a contract between data producers and consumers. Producers agree to send data conforming to the schema; consumers can rely on the data meeting those guarantees.

---

## Types of Validation Errors

Schema validation catches several categories of problems:

### Missing Columns

A column defined in the schema does not exist in the record at all. This might happen when:
- An upstream system stops sending a field
- A new required column was added to the schema but not backfilled
- Data serialization issues drop fields

**Error format**: "{column}: missing"

### Null Values in Non-Nullable Columns

The column exists but contains a null value when the schema says nulls are not allowed. This might happen when:
- An upstream system sends null instead of a proper value
- Data parsing fails and defaults to null
- A required field was left empty in a form submission

**Error format**: "{column}: null"

### Type Mismatches

The value exists but has the wrong type. For example, a string "abc" in a column expecting an integer, or a boolean where a float is expected. This might happen when:
- Data serialization issues convert types
- User input is not properly validated upstream
- Different systems use different type conventions

**Error format**: "{column}: expected {type}, got {actual_type}"

### Out-of-Range Values

The value has the correct type but falls outside acceptable bounds. For example, a negative age or a percentage above 100. This might happen when:
- Data entry errors
- Unit conversion mistakes
- Sensor malfunctions producing impossible readings

**Error format**: "{column}: out of range"

---

## Validation Order and Short-Circuiting

Validation checks are performed in a specific order for each column:

**Step 1: Check if column exists**
If the column is missing from the record, report "missing" error and skip all further checks for this column.

**Step 2: Check for null (if column is not nullable)**
If the value is null and the column does not allow nulls, report "null" error and skip further checks.

**Step 3: Check type**
If the value type does not match the expected type, report "type" error and skip the range check.

**Step 4: Check range (if bounds are specified)**
If the value falls outside [min, max], report "out of range" error.

This short-circuiting approach ensures:
- Error messages are specific and actionable
- You do not get cascading errors (e.g., "type error" followed by "range error" for a null value)
- Processing is efficient (skip checks that cannot pass)

---

## Type Checking Details

Type validation has some nuances:

**Integer Type ("int")**: Accepts Python int values. Does NOT accept floats (even 1.0) or booleans (even though bool is a subclass of int in Python). Use `type(value) == int` rather than `isinstance(value, int)` to exclude booleans.

**Float Type ("float")**: Accepts both Python float and int values. This is because integers can be safely treated as floats mathematically. Use `type(value) in (int, float)`.

**String Type ("str")**: Accepts Python str values only.

The distinction between `type()` and `isinstance()` matters because in Python, `bool` is a subclass of `int`. Using `isinstance(True, int)` returns True, which would incorrectly accept booleans in integer columns.

---

## Handling Nullable Columns

When a column is marked as nullable:
- If the value is None, the record passes validation for that column (skip type and range checks)
- If the value is not None, proceed with type and range checks as normal

This allows optional fields where missing data is acceptable and does not indicate an error.

---

## Range Checking

Range checks apply only to numeric columns with defined bounds:

$$
\text{valid} = (\text{min} \leq \text{value} \leq \text{max})
$$

Both bounds are inclusive. A value exactly equal to min or max passes the check.

Range checks are only performed if:
1. The column exists
2. The value is not null
3. The value has the correct type
4. The schema defines min and/or max bounds for this column

If only min is defined, check value >= min. If only max is defined, check value <= max.

---

## Processing Multiple Columns

For each record, columns are validated in schema order (the order columns appear in the schema definition). This deterministic ordering ensures consistent error reporting.

A single record can have errors in multiple columns. All columns are checked (subject to short-circuiting within each column), and all errors are collected.

The record is valid only if all columns pass all their applicable checks.

---

## A Detailed Worked Example

**Schema:**
- Column "user_id": type="int", nullable=false
- Column "age": type="int", nullable=false, min=0, max=150
- Column "score": type="float", nullable=true, min=0.0, max=100.0
- Column "name": type="str", nullable=false

**Record 1:** {"user_id": 123, "age": 25, "score": 85.5, "name": "Alice"}

Validation:
- user_id: exists, not null, type(123)==int (yes), no range. PASS
- age: exists, not null, type(25)==int (yes), 0<=25<=150 (yes). PASS
- score: exists, not null (allowed), type(85.5)==float (yes), 0<=85.5<=100 (yes). PASS
- name: exists, not null, type("Alice")==str (yes). PASS

Result: (0, True, [])

**Record 2:** {"user_id": "abc", "age": -5, "score": None, "name": "Bob"}

Validation:
- user_id: exists, not null, type("abc")==int? No, type is str. ERROR: "user_id: expected int, got str"
- age: exists, not null, type(-5)==int (yes), 0<=-5? No. ERROR: "age: out of range"
- score: exists, value is None, column is nullable. PASS (skip type and range checks)
- name: exists, not null, type("Bob")==str (yes). PASS

Result: (1, False, ["user_id: expected int, got str", "age: out of range"])

**Record 3:** {"user_id": 456, "score": 75.0, "name": "Carol"}

Validation:
- user_id: exists, not null, type ok. PASS
- age: MISSING. ERROR: "age: missing"
- score: exists, not null, type(75.0)==float (yes), range ok. PASS
- name: exists, not null, type ok. PASS

Result: (2, False, ["age: missing"])

**Record 4:** {"user_id": 789, "age": None, "score": 50, "name": ""}

Validation:
- user_id: PASS
- age: exists, value is None, column is NOT nullable. ERROR: "age: null"
- score: exists, value=50, type(50)==float? Need to check int too. type(50)==int, and float accepts int. PASS. 0<=50<=100. PASS
- name: exists, value="", not null (empty string is not null), type("")==str (yes). PASS

Result: (3, False, ["age: null"])

---

## The Output Format

The validation function returns a list of tuples, one per record:

$$
(\text{record\_index}, \text{is\_valid}, \text{errors})
$$

- **record_index**: 0-based position of the record in the input list
- **is_valid**: Boolean indicating whether the record passed all checks
- **errors**: List of error message strings (empty if valid)

This format allows downstream code to easily:
- Filter to valid records for loading
- Route invalid records to a dead-letter queue
- Generate detailed error reports for data quality monitoring

---

## Why Schema Validation Matters

**Early Detection**: Catching problems at ingestion prevents them from spreading through the entire data ecosystem.

**Clear Contracts**: Schemas make data expectations explicit, reducing confusion between teams.

**Debugging Aid**: Specific error messages pinpoint exactly what is wrong, speeding up root cause analysis.

**Data Quality Metrics**: Tracking validation pass rates over time reveals trends in upstream data quality.

**Compliance**: Many regulations require demonstrating data integrity, which schema validation supports.

---

## Where Schema Validation Shows Up

**ETL Pipelines**: Every major ETL framework (Apache Spark, Apache Beam, dbt, Airflow) supports schema validation as a core feature.

**API Gateways**: Incoming API requests are validated against OpenAPI/Swagger schemas before processing.

**Data Warehouses**: Modern warehouses (Snowflake, BigQuery, Redshift) can enforce schema constraints at load time.

**Event Streaming**: Kafka Schema Registry ensures that event producers and consumers agree on data formats.

**Machine Learning Pipelines**: Feature engineering code validates inputs before computing features to prevent garbage-in-garbage-out.