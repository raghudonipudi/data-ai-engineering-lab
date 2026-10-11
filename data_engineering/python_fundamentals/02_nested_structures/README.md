# Drills: Nested Data Structures (list of dicts)

Five short, isolated drills on the pattern you flagged as the weak spot —
constructing and manipulating a list of dicts. Each one is a SQL operation
you already know cold, just done by hand in Python instead of by a query
engine.

| Python task | SQL equivalent |
| --- | --- |
| `sorted(rows, key=...)` | `ORDER BY` |
| filtering rows with a condition | `WHERE` |
| pulling one field out of every row | `SELECT column` |
| grouping rows by a key | `GROUP BY` |

## The data

All drills use the same small toy dataset defined at the top of
`drills.py` — no file I/O, no CSV, just a plain Python list of dicts so you
can focus on the structure itself.

## The drills

Each function in `drills.py` has a docstring stating the goal and its SQL
equivalent. Fill in each one, then run the file — `main()` prints the
result of each drill so you can eyeball whether it looks right.

1. `sort_by_value` — `ORDER BY reading_value`
2. `sort_by_two_keys` — `ORDER BY sensor_id, reading_value DESC`
3. `filter_above` — `WHERE reading_value > 70`
4. `extract_values` — `SELECT reading_value` (just the numbers, no dicts)
5. `group_by_sensor` — `GROUP BY sensor_id`

No need to do them in order — jump to whichever feels like the actual gap.

## Running it

```bash
C:\Raghu\de-practice\.venv\Scripts\python.exe drills.py
```
