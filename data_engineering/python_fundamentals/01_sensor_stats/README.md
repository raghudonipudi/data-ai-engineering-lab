# Exercise 1: Sensor Readings Summary

## Scenario

You've got a CSV export of temperature sensor readings from two manufacturing
plants (`sensor_readings.csv`, in this same folder). This is the kind of raw
file a DE pipeline would ingest before loading into a Delta table.

Columns: `sensor_id, plant_location, timestamp, reading_value`

The data is messy on purpose:

- One row has a **missing** `reading_value`.
- One row has an **outlier** value (300.0 — clearly a bad sensor reading,
  normal range for these sensors is roughly 50-90).

## Task

Write a Python script `exercise.py` (starter file already created for you)
that:

1. Reads `sensor_readings.csv`.
2. Skips/handles rows with a missing `reading_value` (don't crash, don't
   count them as 0).
3. Filters out obvious outliers (values outside 0-150) before computing
   stats — but print a warning listing which rows got dropped and why.
4. Computes, **per `sensor_id`**: count of valid readings, average, min, max.
5. Prints a clean summary table to the console, sorted by `sensor_id`.
6. Writes the same summary to `summary.csv` in this folder with columns:
   `sensor_id, plant_location, count, avg, min, max`.

## Constraints (this is the point of the exercise)

- Use only the Python standard library (`csv`, no pandas) — the goal is to
  practice core Python: loops, dicts, functions, string/number handling,
  file I/O.
- Structure it with functions, not one long script top to bottom — at
  minimum separate "read + clean data" from "compute stats" from "write
  output".
- Add a docstring or comment only where the *why* isn't obvious — don't
  narrate every line.

## When you're done

Just let me know / paste the file (or tell me to read it) and I'll review it —
I won't rewrite it for you, I'll point out what to fix or do differently and
why, then you take another pass.

## Running it

```bash
python exercise.py
```
