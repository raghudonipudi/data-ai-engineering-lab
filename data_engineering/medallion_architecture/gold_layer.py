from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import pandas as pd
from bronze_layer import customers_transform, products_transform, orders_transform
from silver_layer import silver_transformations

customers_raw_csv = "/Volumes/Transcend/data-ai-engineering-lab/data-samples/medallion_architecture/customers_raw.csv"
products_raw_csv = "/Volumes/Transcend/data-ai-engineering-lab/data-samples/medallion_architecture/products_raw.csv"
orders_raw_csv = "/Volumes/Transcend/data-ai-engineering-lab/data-samples/medallion_architecture/orders_raw.csv"

cust_pdf = pd.read_csv(customers_raw_csv)
prod_pdf = pd.read_csv(products_raw_csv)
orders_pdf = pd.read_csv(orders_raw_csv)

cust_pdf = customers_transform(cust_pdf)
prod_pdf = products_transform(prod_pdf)
orders_pdf = orders_transform(orders_pdf)

orders_cust_prod_pdf = silver_transformations(cust_pdf, prod_pdf, orders_pdf)
##print(orders_cust_prod_pdf)

spark = SparkSession.builder.appName("Typical ETL Pipeline").getOrCreate()

df = spark.createDataFrame(orders_cust_prod_pdf)
df = df.withColumns({
    "region": F.when(F.col("region") == "NaN", "unknown").otherwise(F.col("region")),
    "phone": F.when(F.col("phone") == "", "unknown").otherwise(F.col("phone"))
})
#df.select("year","month","region","order_id","order_amount_computed","order_value").show()

aggregated_df = df.groupBy("year","month","region","order_value").agg(F.count("order_id").alias("order_count"), F.sum("order_amount_computed").alias("total_revenue"), F.avg("order_amount_computed").alias("avg_order_value"))

aggregated_df.write.parquet("/Volumes/Transcend/data-ai-engineering-lab/data-samples/medallion_architecture/aggregated_orders.parquet", mode="overwrite")

aggregated_df = spark.read.parquet("/Volumes/Transcend/data-ai-engineering-lab/data-samples/medallion_architecture/aggregated_orders.parquet")
aggregated_df.show()

