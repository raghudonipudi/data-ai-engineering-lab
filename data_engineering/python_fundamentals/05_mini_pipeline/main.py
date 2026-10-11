from io_utils import read_records, write_records
from validate import is_valid
from transform import clean_amount, enrich_record


def run_pipeline():
    records = read_records()
    result = []
    for r in records:
        if not is_valid(r):
            continue
        cleaned = clean_amount(r)
        if cleaned is not None:
            enriched = enrich_record(cleaned)
            result.append(enriched)
    write_records(result)


if __name__ == "__main__":
    run_pipeline()
