"""
Exercise 10: Data Quality Audit (lists, dicts, tuples, sets)
See README.md in this folder for the full task description.

Fill in the functions below. Run with:
    python exercise.py
"""

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame

ORDERS_FILE = "orders_clean.csv"


def get_spark():
    return SparkSession.builder.appName("data_quality_audit").master("local[*]").getOrCreate()


def load_orders(spark) -> DataFrame:
    return spark.read.csv(ORDERS_FILE, header=True, inferSchema=True)


def build_audit_config() -> dict:
    """Return a config dict: allowed_regions (set), min_total, max_total."""
    raise NotImplementedError


def validate_region(df: DataFrame, config: dict) -> tuple[DataFrame, list]:
    """Flag rows whose region isn't in config['allowed_regions']. Return (df, warnings list)."""
    raise NotImplementedError


def validate_total_range(df: DataFrame, config: dict, warnings: list) -> list:
    """Append warnings for rows outside [min_total, max_total] to the given list. Return it."""
    raise NotImplementedError


def unique_customers(df: DataFrame) -> set:
    """Return the set of distinct customer_name values."""
    raise NotImplementedError


def summarize_by_region(df: DataFrame) -> dict:
    """Return {region: (order_count, total_sum)} for each region."""
    raise NotImplementedError


def run_audit(df: DataFrame, config: dict) -> tuple[DataFrame, dict]:
    """Orchestrate the checks above. Return (df, report dict)."""
    raise NotImplementedError


def main():
    spark = get_spark()
    orders = load_orders(spark)
    config = build_audit_config()

    df, report = run_audit(orders, config)

    print("Warnings:")
    for w in report["warnings"]:
        print(f"  - {w}")

    print("\nRegion summary (count, total):")
    for region, (count, total) in report["region_summary"].items():
        print(f"  {region}: count={count}, total={total}")

    print(f"\nUnique customers ({len(report['unique_customers'])}):")
    for name in sorted(report["unique_customers"]):
        print(f"  - {name}")

    print(f"\nTotal orders: {report['total_orders']}")

    spark.stop()


if __name__ == "__main__":
    main()
