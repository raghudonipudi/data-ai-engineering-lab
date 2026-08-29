# Exercise 8: Joins + Window Functions

## Scenario

Two tables this time, in this folder:

- `orders_clean.csv` — `order_id, customer_name, region, order_date, total`
  (already-cleaned order data, no sanitization needed — that skill is
  covered by `06`/`07`, this exercise is only about joins and window
  functions).
- `regions_lookup.csv` — `region, regional_manager, quarterly_target`
  (a small dimension table, one row per region).

Note: `North` has a **tie** — orders `2006` and `2007` both have
`total = 600.00`. That's deliberate — see the ranking task below.

## Task

Write two versions of the same logic: `exercise_pandas.py` and
`exercise_pyspark.py` (both starter files already created).

1. **Join**: left-join `orders_clean` with `regions_lookup` on `region`,
   so every order row gains `regional_manager` and `quarterly_target`.
2. **Window function 1 — rank**: add a column `region_rank` — the rank
   of each order by `total` (descending) **within its region**. So the
   highest-total order in each region gets rank 1, independently per
   region (not a global rank across all orders).
   - Decide deliberately: for the `North` tie (`2006`/`2007`, both 600),
     do you want them to get the *same* rank (both rank 1, next order
     jumps to rank 3), or *different* ranks (1 and 2, arbitrarily
     broken)? Both pandas and PySpark support either behavior — look up
     the difference between `rank()` and `dense_rank()` in PySpark, and
     `method="min"` vs `method="first"` in pandas' `.rank()`. Pick one
     and be able to explain why.
3. **Window function 2 — running total**: add a column `running_total` —
   the cumulative sum of `total`, **within each region**, ordered by
   `order_date` ascending. So for a region with 3 orders in date order,
   `running_total` should be `total1`, `total1+total2`, `total1+total2+total3`.
4. **Report**: print (or return) just the rank-1 order per region — the
   top order per region, with its `regional_manager` attached. This is
   the actual point of doing the join + rank together: "who's the top
   customer per region, and who manages that region."

Expected shape of the final joined+enriched table (columns, not exact
values):

```text
order_id, customer_name, region, order_date, total, regional_manager,
quarterly_target, region_rank, running_total
```

## Constraints

- pandas doesn't have SQL-style `OVER (PARTITION BY ... ORDER BY ...)`
  syntax — the equivalent is `.groupby(...)` combined with `.rank()` /
  `.cumsum()`. Find the right combination yourself rather than looking
  up a copy-paste answer — this is the actual translation skill the
  exercise is testing.
- PySpark **does** have real window functions:
  `from pyspark.sql import Window`, then `F.rank().over(window_spec)`
  and `F.sum(...).over(window_spec)`. This is much closer to SQL syntax
  than pandas' approach — notice that difference as you write both.

## When you're done

Paste the file or tell me to read it — same review process as always.

## Running it

```bash
python exercise_pandas.py
python exercise_pyspark.py
```
