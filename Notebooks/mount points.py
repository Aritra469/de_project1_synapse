# Databricks notebook source
dbutils.secrets.listScopes()


# COMMAND ----------

dbutils.secrets.list("kv-scope")

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": "c29ad65f-6614-48a9-92a4-d771a9749333",
          "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope="kv-scope",key="db-service-principal-secret"),
          "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/55df43a2-dbce-4c14-a2e5-51a338012372/oauth2/token"}

# Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = "abfss://storage@synapsesa469.dfs.core.windows.net/",
  mount_point = "/mnt/storage",
  extra_configs = configs)
