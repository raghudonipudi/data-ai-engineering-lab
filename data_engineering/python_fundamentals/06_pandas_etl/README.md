# Exercise 6: Pandas ETL — Sanitize, Normalize, Aggregate

## Scenario

`raw_orders.csv` (in this folder) is a raw export of order data, the kind of
file a DE pipeline would ingest before loading into a bronze/silver table.
It is messy on purpose — this exercise builds on the pattern in
`data_engineering/02_pandas_transformations/etl_pandas.py`, but adds a real
sanitization/normalization step before the aggregation.

Columns: `order_id, customer_name, region, order_date, price, quantity`

Known issues in the raw data:

- Inconsistent casing and stray whitespace in `customer_name` and `region`
  (`" john smith"`, `"JANE DOE"`, `" east "`, `"WEST"`).
- `price` is a string with a `$` and sometimes a thousands comma
  (`"$1,200.50"`), not a usable number.
- One row has a missing `price`.
- One row has a `price` that isn't a number at all (`"not_a_price"`).
- `order_date` is in two different formats: `YYYY-MM-DD` and `MM/DD/YYYY`.
- One `order_id` appears twice with identical data — a duplicate ingestion.
- `quantity` has an invalid negative value in one row and a zero in another.

## Task

Write `exercise.py` (starter file already created for you) using **pandas**
that:

1. **Loads** `raw_orders.csv` into a DataFrame.
2. **Sanitizes**:
   - Trim whitespace from `customer_name` and `region`.
   - Standardize `region` to a consistent casing (e.g. `Title Case`) so
     `"WEST"`, `" west "`, and `"West"` all become the same value.
   - Drop exact duplicate orders (same `order_id`).
   - Drop rows with an unusable `price` (missing or non-numeric) — print
     which `order_id`s got dropped and why.
   - Drop rows with `quantity <= 0` — print which `order_id`s got dropped
     and why.
3. **Normalizes**:
   - Convert `price` into a proper numeric column (strip `$` and `,`).
   - Parse `order_date` into a single consistent date type, regardless of
     which of the two input formats it started in.
   - Add a computed `total` column (`price * quantity`).
4. **Aggregates**: total `total` revenue by `region` and month (same shape
   of output as `02_pandas_transformations/etl_pandas.py` — group by
   year/month, but by `region` too here).
5. Writes the cleaned, normalized order-level data to `clean_orders.csv`,
   and the aggregated summary to `region_month_summary.csv`.

## Constraints (this is the point of the exercise)

- Use **pandas** — this is meant to build your pandas fluency, not
  standard-library CSV handling like the earlier exercises.
- Structure it with functions (e.g. `load_raw`, `sanitize`, `normalize`,
  `aggregate`, `main`) rather than one flat script top-to-bottom.
- Don't silently drop bad rows — always print/log what was dropped and why,
  the same discipline as the mini_pipeline exercise.

## When you're done

Paste the file or tell me to read it, and I'll review — same as always,
I'll point out what to fix and why rather than rewriting it for you.

## Running it

```bash
python exercise.py
```
