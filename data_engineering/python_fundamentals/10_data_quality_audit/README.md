# Exercise 10: Data Quality Audit (lists, dicts, tuples, sets)

## Scenario

This exercise isn't about new PySpark mechanics — it's about how you pass
data *between your own functions*, using the right container type for
each job: a `dict` for config, a `set` for membership checks and
deduplication, a `list` for accumulating results, a `tuple` for a fixed,
immutable multi-value return. Real pipelines constantly need to carry an
"audit trail" (warnings, counts, summaries) alongside the DataFrame
itself — that's what this builds.

`orders_clean.csv` has three deliberately bad rows to catch:

- `2011` — region `"Central"` isn't a real region.
- `2012` — `total = 15.00`, suspiciously low.
- `2013` — `total = 9500.00`, suspiciously high.

## Task

Write `exercise.py` (starter file already created) with **exactly these
function signatures** — the types are the point of the exercise, not a
suggestion:

1. `build_audit_config() -> dict` — returns a config dict with three
   keys: `"allowed_regions"` (a **set** of the four real region names),
   `"min_total"` (50), `"max_total"` (5000).

2. `validate_region(df, config: dict) -> tuple[DataFrame, list[str]]` —
   using `config["allowed_regions"]` (a **set**, so use `in` for an O(1)
   membership check, not a list), find rows whose region isn't allowed.
   Return the **unmodified** `df` plus a **list** of warning strings,
   one per bad row, like
   `"order 2011: region 'Central' not in allowed_regions"`.

3. `validate_total_range(df, config: dict, warnings: list) -> list` —
   takes the **same `warnings` list** from step 2 and appends more
   warnings to it for rows outside `[min_total, max_total]`, then
   **returns that list**. Notice this function receives a list built by
   another function and keeps extending it — that's deliberate: get
   comfortable with a container being threaded through multiple
   functions instead of only ever building one at a time.

4. `unique_customers(df) -> set[str]` — return the **set** of distinct
   `customer_name` values (two customers appear twice in the data —
   your set should show each name once).

5. `summarize_by_region(df) -> dict[str, tuple[int, float]]` — a **dict**
   mapping each region to a **tuple** `(order_count, total_sum)`. E.g.
   `{"West": (4, 2465.0), ...}`.

6. `run_audit(df, config: dict) -> tuple[DataFrame, dict]` — orchestrates
   1-5, and returns `(df, report)` where `report` is a dict with keys
   `"warnings"` (list), `"region_summary"` (dict of tuples),
   `"unique_customers"` (set), `"total_orders"` (int, `df.count()`).

7. In `main()`, call `run_audit`, then print the report in a readable
   way — not just `print(report)` (a raw dict/set dump is unreadable);
   loop over the pieces and format them.

## A specific trap to know about

```python
def bad_example(warnings=[]):   # DON'T do this
    ...
```

A mutable default argument (`[]` or `{}`) is created **once**, when the
function is defined — not fresh on every call. If you ever mutate it,
every future call sees the leftover state from previous calls. This is
one of Python's most common real bugs. None of the signatures above need
a mutable default, but keep this in mind for anything you write yourself
going forward: default to `None` and create the list/dict inside the
function body instead.

## When you're done

Paste the file or tell me to read it — same review process as always.

## Running it

```bash
python exercise.py
```
