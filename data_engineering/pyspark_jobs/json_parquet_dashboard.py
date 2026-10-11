from pyspark.sql import SparkSession
from pyspark.sql.functions import avg
from data_engineering.api_ingestion.transform_layer import do_transform_layer

spark = SparkSession.builder \
        .appName("Hourly Temperature Dashboard") \
        .getOrCreate()

url = "https://api.open-meteo.com/v1/forecast?latitude=17.3850&longitude=78.4867&hourly=temperature_2m,relative_humidity_2m"

##df = spark.range(10)
##df.show()

df = do_transform_layer(url)
df = spark.createDataFrame(df)

df.write.parquet("/Volumes/Transcend/data-ai-engineering-lab/data-samples/hourly_temperature_dashboard.parquet", mode="overwrite")

df = spark.read.parquet("/Volumes/Transcend/data-ai-engineering-lab/data-samples/hourly_temperature_dashboard.parquet")

df = df.groupBy("year", "month", "temp_category").agg(avg("temp").alias("avg_temp")).orderBy("year", "month", "temp_category")

df.write.parquet("/Volumes/Transcend/data-ai-engineering-lab/data-samples/hourly_temperature_dashboard_aggregated.parquet", mode="overwrite")
                                                                                               
df.show()


       
