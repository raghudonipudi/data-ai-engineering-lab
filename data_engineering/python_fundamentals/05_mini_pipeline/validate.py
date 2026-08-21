VALID_REGIONS = {"west", "east", "south"}


def is_valid(record):
    if record.get("region") not in VALID_REGIONS:
        return False
    if record.get("amount") is None:
        return False
    return True
