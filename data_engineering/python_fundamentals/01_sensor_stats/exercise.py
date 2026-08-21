"""
Exercise 1: Sensor Readings Summary
See README.md in this folder for the full task description.

Fill in the functions below. Run with:
    ..\..\.venv\Scripts\python.exe exercise.py
"""

import csv

INPUT_FILE = "sensor_readings.csv"
OUTPUT_FILE = "summary.csv"
VALID_RANGE = (0, 150)


def read_rows(path):
    """Read the CSV and return a list of raw row dicts."""
    with open (path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)



def clean_rows(rows):
    """
    Given raw rows, return only the ones with a usable numeric reading_value
    inside VALID_RANGE. Print a warning for each row you drop, saying why.
    """
    crows = []
    for row in rows:
        if row['reading_value'] != "":
            row['reading_value'] = float(row['reading_value'])
            if row['reading_value'] >= VALID_RANGE[0] and row['reading_value'] < VALID_RANGE[1]:
                crows.append(row)
            else:
                print(f"Row {row} excluded because temperature doesnt fit in the range.")
        else:
            print(f"Row {row} excluded because there is no temperature value.")
    return crows


def compute_stats(rows):
    """
    Given cleaned rows, return a dict keyed by sensor_id, where each value
    is a dict like:
        {"plant_location": ..., "count": ..., "avg": ..., "min": ..., "max": ...}
    """

    cdict = {}
    stats = []

    for row in rows:

        key = (row["sensor_id"], row["plant_location"])

        if key not in cdict:
            cdict[key] = []
        cdict[key].append(row["reading_value"])

    for (sensor_id, plant_location), values in cdict.items():

        astats = {
            "sensor_id": sensor_id,
            "plant_location": plant_location,
            "count": len(values),
            "min": min(values),
            "avg": sum(values)/len(values),
            "max": max(values)

        }
        stats.append(astats)

    return stats


def print_summary(stats):
    """Print the stats dict as a readable table, sorted by sensor_id."""

    result = sorted(stats, key = lambda r: r["sensor_id"])

    
    for row in result:
        print(f"sensor_id:{row["sensor_id"]} plant_location:{row["plant_location"]} count={row["count"]} avg={row["avg"]} min={row["min"]}, max={row["max"]}")

    return result

def write_summary(stats, path):
    """Write the stats dict to a CSV file with the columns described in the README."""

    with open(path, 'w', newline="") as f:

        fieldnames = ["sensor_id", "plant_location", "count", "avg", "min", "max"]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stats)


def main():
    rows = read_rows(INPUT_FILE)
    clean = clean_rows(rows)
    stats = compute_stats(clean)
    stats = print_summary(stats)
    write_summary(stats, OUTPUT_FILE)


if __name__ == "__main__":
    main()
