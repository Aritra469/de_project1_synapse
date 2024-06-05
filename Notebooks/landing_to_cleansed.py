# Databricks notebook source
from pyspark.sql.functions import *
from datetime import datetime,date,timedelta

# COMMAND ----------

today = date.today()
yesterday = today - timedelta(days = 1)
year_str = yesterday.strftime('%Y')
month_str = yesterday.strftime('%m')
day_str = yesterday.strftime('%d')

# COMMAND ----------

base_input_path = "/mnt/storage/Landing/"
input_path = f"{base_input_path}{year_str}/{month_str}/{day_str}/part*"
df = spark.read.json(input_path)

# COMMAND ----------

coin_list = []
coin_list =  df.columns
#new_list=[str(x) for x in coin_list]

# COMMAND ----------

from pyspark.sql.functions import *
def flat_json(df,i):
    return df.select(lit(coin_list[i]).alias("coin_name"),col(f"{coin_list[i]}.inr").alias("coin_price"),col(f"{coin_list[i]}.inr_24h_change").alias("coin_price_change"),col(f"{coin_list[i]}.inr_24h_vol").alias("coin_vol_change"),col(f"{coin_list[i]}.inr_market_cap").alias("coin_market_cap"))

df_final = flat_json(df,0)

for i in range(1,len(coin_list)):
    df1 = flat_json(df,i)
    df_final = df_final.union(df1)


# COMMAND ----------

df_final.show(50)

# COMMAND ----------

base_output_path_cleansed = "/mnt/storage/cleansed/"
output_path_cleansed = f"{base_output_path_cleansed}{year_str}/{month_str}/{day_str}/"
df_final.repartition(1).write.mode('overwrite').csv(output_path_cleansed,header=True)
