import sys
from pyspark.context import SparkContext
from pyspark.sql.functions import col, when, lit, current_timestamp
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions


# 1. Initialize Glue

args = getResolvedOptions(sys.argv, ["JOB_NAME", "INPUT_KEY"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session


# 2. Parameters

BUCKET = "travel-etl-project"
input_key = args["INPUT_KEY"]

input_path = f"s3://{BUCKET}/{input_key}"

# Extract partitions
parts = input_key.split("/")
year = parts[2].split("=")[1]
month = parts[3].split("=")[1]
day = parts[4].split("=")[1]

output_path = f"s3://{BUCKET}/processed/travel_clean/"

# 3. Extract

df = spark.read.option("header", True).csv(input_path)

# 4. Transform

# Fix categorical values
df = df.withColumn(
    "Gender",
    when(col("Gender") == "Fe Male", "Female").otherwise(col("Gender"))
)

df = df.withColumn(
    "MaritalStatus",
    when(col("MaritalStatus") == "Single", "Unmarried").otherwise(col("MaritalStatus"))
)

# Fill missing values
from pyspark.sql.functions import mean

# Median approximation (Spark doesn't have exact median easily)
age_median = df.approxQuantile("Age", [0.5], 0.01)[0]
duration_median = df.approxQuantile("DurationOfPitch", [0.5], 0.01)[0]
trips_median = df.approxQuantile("NumberOfTrips", [0.5], 0.01)[0]
income_median = df.approxQuantile("MonthlyIncome", [0.5], 0.01)[0]

df = df.fillna({
    "Age": age_median,
    "DurationOfPitch": duration_median,
    "NumberOfTrips": trips_median,
    "MonthlyIncome": income_median
})

# Mode approximation (most frequent value)
def get_mode(column):
    return df.groupBy(column).count().orderBy(col("count").desc()).first()[0]

df = df.fillna({
    "TypeofContact": get_mode("TypeofContact"),
    "NumberOfFollowups": get_mode("NumberOfFollowups"),
    "PreferredPropertyStar": get_mode("PreferredPropertyStar"),
    "NumberOfChildrenVisiting": get_mode("NumberOfChildrenVisiting")
})

# Feature Engineering
df = df.withColumn(
    "TotalVisiting",
    col("NumberOfChildrenVisiting") + col("NumberOfPersonVisiting")
)

df = df.drop("NumberOfChildrenVisiting", "NumberOfPersonVisiting")

# 5. Validation (Exact logic)

df = df.dropDuplicates()

df = df.filter(col("Age") > 0)
df = df.filter(col("MonthlyIncome") > 0)
df = df.filter(col("CityTier").isin([1, 2, 3]))


# 6. Metadata Columns

df = df.withColumn("load_timestamp", current_timestamp())

df = df.withColumn("year", lit(year))
df = df.withColumn("month", lit(month))
df = df.withColumn("day", lit(day))

# 7. Load (Append + Partition)

df.write.mode("append") \
    .partitionBy("year", "month", "day") \
    .parquet(output_path)

print("ETL job completed successfully")