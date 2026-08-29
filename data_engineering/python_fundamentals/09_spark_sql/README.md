# Exercise 9: Spark SQL

## Scenario

Same task and same data as `08_joins_window_functions` — join
`orders_clean.csv` with `regions_lookup.csv`, add a rank window function
and a running-total window function, produce a top-order-per-region
report. This time, do it with **actual SQL**, using
`df.createOrReplaceTempView(...)` and `spark.sql("...")`, instead of the
DataFrame method-chaining API from `08`.

The point: you already know SQL deeply (19 years of it). This exercise
is about learning the two or three PySpark-specific mechanics that let
you use that SQL knowledge directly, instead of relearning everything as
DataFrame method calls.

## Task

Write `exercise.py` (starter file already created):

1. **Load** both CSVs into DataFrames, then register each as a temp view
   (`orders.createOrReplaceTempView("orders")`, same for `regions`).
2. **Write one SQL query** (a Python multi-line string passed to
   `spark.sql(...)`) that does everything at once:
   - `LEFT JOIN orders o ON o.region = r.region` against the regions view.
   - `RANK() OVER (PARTITION BY o.region ORDER BY o.total DESC)` as
     `region_rank` — match the tie behavior from `08` (ties share the
     same rank).
   - `SUM(o.total) OVER (PARTITION BY o.region ORDER BY o.order_date
     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` as
     `running_total`.
3. **A second SQL query** (or a `WHERE region_rank = 1` filter on the
   first result, your choice) producing the top-order-per-region report,
   same as `08`.
4. Print both results.

## Constraints

- The join + both window functions must be **actual SQL syntax** inside
  a `spark.sql(...)` call — not `.join()`/`.withColumn()`/`.over()`
  DataFrame methods. This exercise is specifically about the SQL
  interface.
- You can still use Python for orchestration (loading files, registering
  views, printing results) — just not for the transformation logic
  itself.

## When you're done

Paste the file or tell me to read it — same review process as always.

## Running it

```bash
python exercise.py
```
