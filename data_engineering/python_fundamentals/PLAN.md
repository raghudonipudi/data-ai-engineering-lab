# Python / PySpark Fluency Plan

Sub-plan for Month 1 of the main roadmap (`C:\Raghu\ai-engineer-roadmap.md`).
Goal: stop translating between Python and PySpark syntax by feel — build
real recall through repeated, structured translation of the same problems.

**2026-08-22 update:** pandas is deliberately deprioritized for now (was
splitting focus and causing syntax confusion — resequenced, not dropped;
it comes back easily once PySpark is solid, and PySpark reuses pandas
syntax directly via `pandas_udf`/pandas-on-Spark anyway). Steps from here
are Python/PySpark only. Databricks (`../orders_pipeline/SPEC.md` Track A)
is also paused for now — pure language/DataFrame fluency first.

## Steps

- [x] **0. Install a JDK** and set `JAVA_HOME` — done 2026-08-21.
- [x] **06 — Pandas ETL**: sanitize/normalize/aggregate messy order data.
      Done and reviewed on 2026-08-21.
- [x] **07 — PySpark ETL**: same task as 06, rewritten in `pyspark.sql`.
      Done 2026-08-22, sanitize/normalize/aggregate all correct. One
      cosmetic nit outstanding: rename the aggregate output column from
      `total_aggregated` to `total`.
- [x] **08 — Joins + window functions**: `08_joins_window_functions/` —
      join `orders_clean.csv` with `regions_lookup.csv`, `region_rank`
      and `running_total` window functions, in both pandas and PySpark.
      Done 2026-08-22 — both implementations correct and, after review,
      made to agree on tie-breaking (`method="min"` / `F.rank()`, ties
      share the lowest rank).
- [ ] **09 — Spark SQL**: `09_spark_sql/` — same join + window-function
      task as 08, but via `spark.sql(...)` and temp views instead of the
      DataFrame API. Leans on 19 years of SQL background directly.
      **Next immediate step.**
- [ ] **10 — Nested/semi-structured data**: structs, arrays, `explode` —
      common in real ingestion (JSON-like bronze-layer data). Not yet
      created.
- [ ] **11 — Partitioning/caching basics**: not yet created.
- [ ] **Cheat-sheet**: build your own Python/PySpark equivalence table by
      hand as you go — filter, groupby, join, window, dedupe, cast,
      date-parse, null-handling, plus DataFrame-API-vs-SQL now that 09
      covers both. Write it yourself, don't copy one.

## Notes

- Don't skip 0 — PySpark silently fails with `JAVA_GATEWAY_EXITED` without
  a JDK, it's not a code problem.
- Each exercise folder is self-contained (own README, own data) so you can
  come back to any of these independently.
