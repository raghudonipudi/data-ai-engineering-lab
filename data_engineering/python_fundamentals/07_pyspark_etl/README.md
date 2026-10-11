# Exercise 7: PySpark ETL — Same Task, New Syntax

## Scenario

Same `raw_orders.csv`, same task as `06_pandas_etl` — but this time written in
PySpark instead of pandas. The point isn't new logic, it's mapping logic you
already got right once onto a different API, so the translation sticks.

## Prerequisite

PySpark needs a JDK to run locally (it launches a local JVM). Before running
this exercise:

1. Install a JDK (Temurin 17 is a solid free choice:
   [https://adoptium.net](https://adoptium.net)).
2. Set `JAVA_HOME` to point at the install, and make sure `java -version`
   works from a fresh terminal.

If you hit `JAVA_GATEWAY_EXITED` or `Java not found` errors, this step
wasn't completed correctly.

**Windows note**: writing output with Spark's native `.write().csv(...)`
needs a Hadoop utility called `winutils.exe`, which Apache doesn't ship
for Windows. We tried matching community builds for both Hadoop 3.4.x
and 3.3.x — both hit the identical native-method error. Root cause:
**Windows 11's Smart App Control** (enabled by default on fresh installs)
blocks the unsigned `hadoop.dll` from loading properly for `java.exe`.
Since Smart App Control can't be re-enabled once turned off (only via a
full Windows reinstall), we're not disabling it just for this. The
starter code instead materializes final results with
`.toPandas().to_csv(...)` for the two output files only; every actual
transformation (filter, groupBy, dedup, date parsing) is still 100%
PySpark. (Separately: PySpark 3.5.x's `toPandas()` needs the `setuptools`
package installed, since it imports the now-removed stdlib `distutils`
module under Python 3.12 — already in `requirements.txt`.)

## Task

Reimplement the exact same pipeline as `06_pandas_etl/exercise.py`, using
`pyspark.sql` instead of pandas:

1. **Load** `raw_orders.csv` into a Spark DataFrame.
2. **Sanitize**:
   - Trim whitespace and standardize casing on `customer_name`/`region`.
   - Drop duplicate `order_id`s.
   - Drop rows with unusable `price` (missing or non-numeric).
   - Drop rows with `quantity <= 0`.
   - Print/log what got dropped and why (same discipline as before).
3. **Normalize**:
   - Convert `price` to numeric (strip `$` and `,`).
   - Parse `order_date` into a single consistent date type, handling both
     input formats.
   - Add a computed `total` column (`price * quantity`).
4. **Aggregate**: total `total` revenue by `region` and month.
5. Write the cleaned data and the aggregated summary out (Parquet or CSV,
   your call).

## The actual point of this exercise

As you write each step, notice the PySpark equivalent of the pandas call you
already wrote. A few you'll hit:

| Pandas | PySpark |
|---|---|
| `df["col"].str.strip()` | `F.trim(F.col("col"))` |
| `df.drop_duplicates(subset=[...])` | `df.dropDuplicates([...])` |
| `df[df["price"].isna()]` | `df.filter(F.col("price").isNull())` |
| `pd.to_numeric(..., errors="coerce")` | `F.col("price").cast("double")` (invalid → null) |
| `pd.to_datetime(..., format="mixed")` | needs explicit format handling — this one's genuinely harder, think about it |
| `df.groupby([...]).agg(...)` | `df.groupBy(...).agg(...)` |

Don't copy this table into your code — **use it to check yourself**, and add
rows to your own cheat-sheet as you discover more.

## Constraints

- Use `pyspark.sql.functions` (`import pyspark.sql.functions as F`), not
  pandas — if you catch yourself converting to pandas with `.toPandas()`
  partway through, that defeats the point.
- Structure it with functions, same as before.

## When you're done

Paste the file or tell me to read it — same review process as always.

## Running it

```bash
python exercise.py
```
