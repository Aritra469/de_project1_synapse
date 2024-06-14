# Project Details
## Architecture Diagram:
![image](https://github.com/Aritra469/de_project1_synapse/assets/171404393/39152af4-ea2d-4176-aed0-aa95315b73a1)

## Steps:
### Ingestion:
I have used [coingecko api](https://docs.coingecko.com/reference/simple-price) to pull top 5 crypto currency data daily.
pl_coin_price_raw is used to ingest the data from api and then used adls as sink. The file path is written dynamically so that the files contains timestamp when it is ingested.This pipeline is scheduled triggered on hourly basis.
Here is the pipeline image
<img width="958" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/2c9ecbf6-c168-4ad6-9267-b06a081b7ca0">
and the raw files look like this


I have used Azure synapse to ingest data from the api. The activity used here is copy activity and the linked service used
here is http. Sink for the copy activity is Raw folder inside azure datalake container.
<img width="957" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/c6b25191-7e01-4341-ae9f-5c9502f9f25f">
I have used a schedule trigger to occur hourly.So, I will get hourly current data about the coin price.
<img width="955" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/da02f56b-b5b7-4346-9d5f-69cb56ab2dff">

### Transformation:
    Azure Databricks is used for all the transformation steps. After the data received in Raw folder I run a databricks notebook to merge all
    the files for previous day and write them in a single file with a yyyy/mm/dd folder structure within landing folder.Then the json file in 
    landing folder is flattened in required schema and saved as csv file in cleansed folder. After that I perform an aggregation to get daily
    averages and stored them in aggregate folder.

### Vizualization:
    I have used spark SQL to visualize the data and add them to particular dashboards for each coin.




1. ~~Have to automate the cluster termination process.~~
2. Have to collect pipeline success or error message and visualize using serverless sql.
3. Have to move previous months raw data in archive in yyyy/mm/dd or yyyy/mm structure.



