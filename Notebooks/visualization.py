# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import StructType,StructField, StringType, DecimalType, DateType

# COMMAND ----------

schema = StructType([
    StructField("coin_name",StringType(),False),
    StructField("avg_coin_price",DecimalType(18,2),False),
    StructField("avg_coin_price_change",DecimalType(18,2),False),
    StructField("avg_coin_vol_change",DecimalType(18,2),False),
    StructField("avg_coin_market_cap",DecimalType(18,2),False),
    StructField("modified_date",DateType(),False)
  ])

# COMMAND ----------

coin_list = ['binancecoin','bitcoin','ethereum','solana','tether']

# COMMAND ----------

base_input_path = "/mnt/storage/aggregate/"
for name in coin_list:
    input_path = f"{base_input_path}{name}/part*"
    df = spark.read.format("csv").option("header",True).schema(schema).load(input_path)
    df.createOrReplaceTempView(name)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from binancecoin

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bitcoin

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ethereum

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from solana

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from tether
