from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark
spark = SparkSession.builder.appName("NYCTaxi_Processing").getOrCreate()

# Load the data from GCS
input_path = "gs://nyc-taxi-pipeline-amin/raw/*.parquet"
df = spark.read.parquet(input_path)

# Data Cleaning
df_cleaned = df.filter((col("trip_distance") > 0) & (col("total_amount") > 0))

# Save to BigQuery
df_cleaned.write.format("bigquery") \
    .option("table", "midnight-495805.nyc_data.yellow_trips_final") \
    .option("temporaryGcsBucket", "nyc-taxi-pipeline-amin") \
    .mode("overwrite") \
    .save()