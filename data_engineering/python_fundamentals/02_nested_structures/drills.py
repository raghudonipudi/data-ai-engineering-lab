"""
Drills: Nested Data Structures
See README.md for the SQL-equivalent framing for each drill.

Fill in each function, then run:
    ..\..\.venv\Scripts\python.exe drills.py
"""

readings = [
    {"sensor_id": "S-101", "reading_value": 74.8},
    {"sensor_id": "S-103", "reading_value": 81.2},
    {"sensor_id": "S-101", "reading_value": 72.4},
    {"sensor_id": "S-102", "reading_value": 69.5},
    {"sensor_id": "S-103", "reading_value": 80.7},
    {"sensor_id": "S-104", "reading_value": 55.0},
    {"sensor_id": "S-101", "reading_value": 73.1},
    {"sensor_id": "S-104", "reading_value": 54.6},
]


def sort_by_value(rows):
    """
    ORDER BY reading_value

    Return a new list of the same dicts, sorted ascending by reading_value.
    """

    result = sorted(rows, key = lambda r: r["reading_value"])


    return result


def sort_by_two_keys(rows):
    """
    ORDER BY sensor_id, reading_value DESC

    Return a new list sorted by sensor_id ascending, and for rows with the
    same sensor_id, by reading_value descending.
    """

    result = sorted(rows, key = lambda r: (r["sensor_id"], -r["reading_value"]))

    return result




def filter_above(rows, threshold):
    """
    WHERE reading_value > threshold

    Return only the rows whose reading_value is greater than threshold.
    """
    result = []

    for row in rows:

        if row["reading_value"]  > threshold:
            result.append(row)

    return result


def extract_values(rows):
    """
    SELECT reading_value

    Return a plain list of just the reading_value numbers, in the same
    order as rows -- no dicts, no sensor_id, just the numbers.
    """

    result = []

    for row in rows:

        result.append(row["reading_value"])

    return result


def group_by_sensor(rows):
    """
    GROUP BY sensor_id

    Return a dict: {sensor_id: [reading_value, reading_value, ...]}
    """

    result = {}

    for row in rows:

        key = row["sensor_id"]

        if key in result:
            result[key].append(row["reading_value"])
        else:
            result[key] = [row["reading_value"]]

    return result


def main():
    print("sort_by_value:", sort_by_value(readings))
    print("sort_by_two_keys:", sort_by_two_keys(readings))
    print("filter_above(70):", filter_above(readings, 70))
    print("extract_values:", extract_values(readings))
    print("group_by_sensor:", group_by_sensor(readings))


if __name__ == "__main__":
    main()
