# Project Details
## Architecture Diagram:
![image](https://github.com/Aritra469/de_project1_synapse/assets/171404393/39152af4-ea2d-4176-aed0-aa95315b73a1)

## Steps:
### Ingestion:
I have used [coingecko api](https://docs.coingecko.com/reference/simple-price) to pull top 5 crypto currency data daily and Azure synapse to ingest data from the api. The activity used here is copy activity and the linked service used
here is http.The pipeline looks like this
<img width="782" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/39a4979b-9444-4ba2-9716-049dcd681b70">

The filepath of the sink dataset is written dynamically to capture the time when the file is ingested , it will be helpful for future transformation.
<img width="460" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/11f108db-0fda-4097-a01f-e8cb52315ac4">

The Sink for the copy activity is Raw folder inside azure datalake container.
<img width="957" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/c6b25191-7e01-4341-ae9f-5c9502f9f25f">

I have used a schedule trigger to occur hourly.So, I will get hourly current data about the coin price.
<img width="955" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/da02f56b-b5b7-4346-9d5f-69cb56ab2dff">

### Transformation:
I have used databricks notebooks for all the transformation.The transformation pipeline looks like this
<img width="904" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/c254469c-5eda-4565-be38-3be4bdfa9268">
(***pl_raw_to_final_daily***)

**raw_to_landing** notebook is used to merge all the previous day's file into a single file and write it into landing folder in year/month/day file structure.To achieve this
I get the current date first ,then using timedelta() function I get the date of previous day.Then converted it into string and used it for reading files ingested previous
day and write it into year/month/day structure using the string.
<img width="760" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/6fd41a66-7f8f-4ed6-8e82-81fb6b82e453">
(***example_of_file_in_landing***)

**landing_to_cleansed** notebook is used to read the merged json file and flatenned it according to our requirements, then writting it into cleansed folder using the same
year/month/day structure in csv format.
<img width="934" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/d1406d4e-c11a-4b5c-81b4-c18765c0b02a">
<img width="608" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/536c8f48-7593-407c-b8ec-b3c3af49dd20">
(***json and csv format***)

### Vizualization:
I have used spark SQL to visualize the data and add them to particular dashboards for each coin.




1. ~~Have to automate the cluster termination process.~~
2. Have to collect pipeline success or error message and visualize using serverless sql.
3. Have to move previous months raw data in archive in yyyy/mm/dd or yyyy/mm structure.
