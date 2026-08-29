"""
Exercise 7: PySpark ETL - Same Task, New Syntax
See README.md in this folder for the full task description.

Fill in the functions below. Run with:
    python exercise.py
"""

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

INPUT_FILE = "raw_orders.csv"
CLEAN_ORDERS_FILE = "clean_orders.csv"
SUMMARY_FILE = "region_month_summary.csv"


def get_spark():
    return SparkSession.builder.appName("pyspark_etl_exercise").master("local[*]").getOrCreate()


def load_raw(spark, path):
    """Read raw_orders.csv into a Spark DataFrame."""
    df = spark.read.csv(path, header=True)

    return df


def sanitize(df):
    """
    Trim whitespace and standardize casing on customer_name/region,
    drop duplicate order_ids, drop rows with unusable price or
    quantity <= 0. Print what got dropped and why.
    """

    df = df.withColumn("Customer_Name", F.initcap(F.trim(F.col("customer_name"))))
    df = df.withColumn("Region", F.initcap(F.trim(F.col("region"))))
    dup_order_id_dup = df.groupBy("order_id").count().filter("count > 1").select("order_id")
    for order_id in dup_order_id_dup.collect():
        print(f"{order_id} is duplicate")
    df = df.dropDuplicates(["order_id"])
    df = df.withColumn("price", F.regexp_replace("price", "\\$|,", ""))
    df = df.withColumn("price", F.when(F.col("price").rlike("^[0-9.]+$"), F.col("price").cast("double")).otherwise(None))
    bad_price_df = df.filter(F.col("price").isNull()).select("order_id")
    for order_id in bad_price_df.collect():
        print(f"{order_id} has a Null price")
    df = df.filter(F.col("price").isNotNull())
    bad_quantity_df = df.filter(F.col("quantity") <= 0 ).select("order_id")
    for order_id in bad_quantity_df.collect():
        print(f"{order_id} has a invalid value")
    df = df.filter(F.col("quantity") > 0)
    return df


def normalize(df):
    """
    Convert price to numeric, parse order_date into a single consistent
    date type (handle both input formats), add a computed total column.
    """
    df = df.withColumn("order_date", F.coalesce(F.to_date(F.expr("try_to_timestamp(order_date, 'yyyy-MM-dd')")), F.to_date(F.expr("try_to_timestamp(order_date, 'MM/dd/yyyy')"))))
    df = df.withColumn("total", F.col("price") * F.col("quantity"))
    return df


def aggregate(df):
    """Return total `total` revenue grouped by region and month."""
    df = df.withColumn("year", F.year("order_date")).withColumn("month", F.month("order_date"))
    df = df.groupBy("region","year", "month").agg(F.sum("total").alias("total"))
    return df


def main():
    spark = get_spark()
    raw = load_raw(spark, INPUT_FILE)
    clean = sanitize(raw)
    normalized = normalize(clean)
    normalized.toPandas().to_csv(CLEAN_ORDERS_FILE, index=False)

    summary = aggregate(normalized)
    summary.toPandas().to_csv(SUMMARY_FILE, index=False)
    summary.show()

    spark.stop()


if __name__ == "__main__":
    main()
