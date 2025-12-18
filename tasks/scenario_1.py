def validate_data(data):
    """
    Validate a list of dictionaries that must contain an integer 'age'.

    Args:
        data (list): list of dicts, e.g. [{"name":"Alice","age":30}, ...]

    Returns:
        list: list of invalid items. Each item is a dict with:
              - "index": position in the original list
              - "entry": the original entry
              - "reason": why it's invalid
    """
    invalid = []
    for idx, item in enumerate(data):
        # item must be a dict
        if not isinstance(item, dict):
            invalid.append({"index": idx, "entry": item, "reason": "not a dict"})
            continue

        # 'age' key must exist
        if "age" not in item:
            invalid.append({"index": idx, "entry": item, "reason": "missing 'age' key"})
            continue

        age = item["age"]
        # exclude booleans (bool is subclass of int in Python)
        if isinstance(age, bool) or not isinstance(age, int):
            invalid.append({"index": idx, "entry": item, "reason": "'age' is not an int"})
            continue

        # optional rule: reject negative ages (uncomment if needed)
        if age < 0:
            invalid.append({"index": idx, "entry": item, "reason": "age is negative"})

    return invalid



data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": "25"},
    {"name": "Charlie"},               # missing age
    {"name": "Dinesh", "age": -2},     # valid by strict type (int) but negative
    {"name": "Esha", "age": True},     # boolean (invalid)
    "not a dict"
]

print(validate_data(data))
