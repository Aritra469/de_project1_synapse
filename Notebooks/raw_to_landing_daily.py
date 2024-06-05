# Databricks notebook source
from pyspark.sql.functions import *

# COMMAND ----------

from datetime import datetime,date,timedelta

# COMMAND ----------

today = date.today()
yesterday = today - timedelta(days = 1)
yesterday_str = yesterday.strftime("%Y-%m-%d")
year_str = yesterday.strftime('%Y')
month_str = yesterday.strftime('%m')
day_str = yesterday.strftime('%d')

# COMMAND ----------

base_input_path = "/mnt/storage/raw/coinprice/"
input_path_pattern = f"{base_input_path}price_{yesterday_str}*.json"
df = spark.read.json(input_path_pattern)
base_output_path = "/mnt/storage/Landing/"
output_path = f"{base_output_path}{year_str}/{month_str}/{day_str}/"
df.repartition(1).write.mode('overwrite').json(output_path)
