def clean_amount(record):
    try:
        record["amount"] = int(record["amount"])
        return record
    except (TypeError, ValueError):
        return None


def enrich_record(record):
    record["amount_category"] = "high" if int(record["amount"]) > 100 else "low"
    return record

