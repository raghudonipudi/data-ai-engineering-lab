"""
Exercise 9: Spark SQL
See README.md in this folder for the full task description.

Fill in the functions below. Run with:
    python exercise.py
"""

from pyspark.sql import SparkSession

ORDERS_FILE = "orders_clean.csv"
REGIONS_FILE = "regions_lookup.csv"


def get_spark():
    return SparkSession.builder.appName("spark_sql_exercise").master("local[*]").getOrCreate()


def load_and_register_views(spark):
    """Load both CSVs and register them as temp views ('orders', 'regions')."""
    orders = spark.read.csv(ORDERS_FILE, header=True, inferSchema=True)
    regions = spark.read.csv(REGIONS_FILE, header=True, inferSchema=True)
    orders.createOrReplaceTempView("orders")
    regions.createOrReplaceTempView("regions")
    return orders, regions


def run_enriched_query(spark):
    """
    Run one spark.sql(...) query: join orders+regions, add region_rank
    (RANK() OVER ...) and running_total (SUM() OVER ...). Return the result DataFrame.
    """
    df =  spark.sql("""
    SELECT o.*, r.regional_manager, RANK() OVER (PARTITION BY o.region ORDER BY o.total DESC) AS region_rank,
    SUM(o.total) OVER (PARTITION BY o.region ORDER BY o.order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
    FROM orders o left join regions r on o.region = r.region""")
    df.createOrReplaceTempView("enriched_df")
    return df


def run_top_order_query(spark):
    """Return the top-order-per-region report, via SQL."""
    df = spark.sql("""
    SELECT region, order_id, customer_name, total, regional_manager from enriched_df WHERE region_rank = 1""")
    return df


def main():
    spark = get_spark()
    load_and_register_views(spark)

    enriched = run_enriched_query(spark)
    enriched.show()

    top = run_top_order_query(spark)
    print("Top order per region:")
    top.show()

    spark.stop()


if __name__ == "__main__":
    main()
