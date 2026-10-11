"""
Exercise 8: Joins + Window Functions (PySpark)
See README.md in this folder for the full task description.

Fill in the functions below. Run with:
    python exercise_pyspark.py
"""

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.window import Window

ORDERS_FILE = "orders_clean.csv"
REGIONS_FILE = "regions_lookup.csv"


def get_spark():
    return SparkSession.builder.appName("joins_window_exercise").master("local[*]").getOrCreate()


def load_data(spark):
    orders = spark.read.csv(ORDERS_FILE, header=True, inferSchema=True)
    regions = spark.read.csv(REGIONS_FILE, header=True, inferSchema=True)
    return orders, regions


def join_orders_with_regions(orders, regions):
    """Left-join orders with the regions lookup table on region."""
    df = orders.join(regions, on="region", how="left")
    return df


def add_region_rank(df):
    """Add region_rank: rank of each order by total (desc), within its region."""
    w = Window.partitionBy("region").orderBy(F.col("total").desc())
    df = df.withColumn("region_rank", F.rank().over(w))
    return df


def add_running_total(df):
    """Add running_total: cumulative sum of total within each region, ordered by order_date."""
    w = Window.partitionBy("region").orderBy("order_date").rowsBetween(Window.unboundedPreceding, Window.currentRow)
    df = df.withColumn("running_total", F.sum("total").over(w))
    return df


def top_order_per_region(df):
    """Return just the rank-1 order per region, with regional_manager attached."""
    df = df.filter(F.col("region_rank") == 1).select("region", "order_id", "customer_name", "total", "regional_manager")
    return df


def main():
    spark = get_spark()
    orders, regions = load_data(spark)
    df = join_orders_with_regions(orders, regions)
    df = add_region_rank(df)
    df = add_running_total(df)
    df.show()

    top = top_order_per_region(df)
    print("Top order per region:")
    top.show()

    spark.stop()


if __name__ == "__main__":
    main()
