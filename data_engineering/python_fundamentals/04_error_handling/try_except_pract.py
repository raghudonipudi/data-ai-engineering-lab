##Exercise: Here's a list of "raw" records where some are malformed:
"""
Write a function clean_amounts(records) that:

Converts amount to an int where possible
Skips (or logs) any record where amount is missing, None, or not a valid number — but doesn't crash the whole script
Returns a list of only the valid, cleaned records, e.g.:

[{"id": 1, "amount": 100}, {"id": 4, "amount": 250}]
"""

def clean_amounts(data):

    result = []

    for row in data:

        try:
            result.append({"id": row["id"], "amount": int(row["amount"])})
        except Exception as e:
            print(f"{row["id"]} is not valid because of {e}")

    return result

records = [
    {"id": 1, "amount": "100"},
    {"id": 2, "amount": "abc"},
    {"id": 3},
    {"id": 4, "amount": "250"},
    {"id": 5, "amount": None},
]


print(clean_amounts(records))