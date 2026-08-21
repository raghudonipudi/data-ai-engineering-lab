# Mini Pipeline Exercise

A small multi-file pipeline for practicing code reading and tracing bugs
across files, not just writing isolated functions.

## Files

- `io_utils.py` — `read_records()` returns fake source data,
  `write_records()` prints the final output.
- `validate.py` — `is_valid()` filters records by region and checks that
  `amount` is not `None`.
- `transform.py` — `clean_amount()` converts `amount` to an `int`,
  `enrich_record()` tags each record as `"high"` or `"low"`.
- `main.py` — orchestrates the pipeline: read, validate, clean, enrich,
  write.

## Task

Run the pipeline:

```bash
python main.py
```

It will crash. Before fixing anything:

1. Read the traceback and identify which record causes the failure.
2. Trace across the files to understand why that record passed
   validation but still broke a later step.
3. Fix the code so the pipeline runs cleanly for all valid records
   without crashing.

The goal is tracing data flow through multiple files, not just patching
the line where the error appears.
