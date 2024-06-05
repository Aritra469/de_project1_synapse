# Databricks notebook source
from pyspark.sql.functions import *
from datetime import datetime,date,timedelta
from pyspark.sql.types import DecimalType,DateType
import os

# COMMAND ----------

today = date.today()
yesterday = today - timedelta(days = 1)
year_str = yesterday.strftime('%Y')
month_str = yesterday.strftime('%m')
day_str = yesterday.strftime('%d')

# COMMAND ----------

base_input_path = "/mnt/storage/cleansed/"
input_path = f"{base_input_path}{year_str}/{month_str}/{day_str}/part*"
df = spark.read.csv(input_path,header=True)

# COMMAND ----------

df.show()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

for i in df.columns[1:]:
    print(i,type(i))

# COMMAND ----------

type(col("coin_price"))


# COMMAND ----------

for name in df.columns[1:]:
    df = df.withColumn(name, col(name).cast(DecimalType(18, 2)))

# COMMAND ----------

df.show(25)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

agg_expressions = []
for name in df.columns[1:]:
    agg_expressions.append(avg(name).alias(f"avg_{name}"))

df_agg = df.groupBy(df.columns[0]).agg(*agg_expressions)

# COMMAND ----------

for name in df_agg.columns[1:]:
    df_agg = df_agg.withColumn(name, round(df_agg[name], 2))

# COMMAND ----------

df_agg.show()

# COMMAND ----------

base_output_path_agg = "/mnt/storage/aggregate/"

def file_exists(path):
    try:
        dbutils.fs.ls(path)
        return True
    except Exception as e:
        return False

for row in df_agg.select("coin_name").collect():
    name = row["coin_name"]
    df_new = df_agg.filter(df_agg.coin_name == name)
    df_new = df_new.withColumn("modified_date", lit(yesterday))
    output_path_agg = f"{base_output_path_agg}{name}/"
    if file_exists(output_path_agg):
        # Read the existing CSV file
        existing_df = spark.read.option("header", "true").csv(f"{output_path_agg}part*")
        
        # Union the new DataFrame with the existing DataFrame
        combined_df = existing_df.union(df_new)
    else:
        # If the file does not exist, the combined DataFrame is just the new DataFrame
        combined_df = df_new
    combined_df.repartition(1).write.mode('overwrite').csv(output_path_agg, header=True)
