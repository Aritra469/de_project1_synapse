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

**cleansed to aggregate** notebook is used to read data from cleansed folder and do some minimal transformations.All numerical columns have casted from string to decimal
type and then aggregated to get average.Then I created a function which will check if the file exists or not in output file path.If file exists in output path then the file
will be read and current aggregated data will be appended on existing file otherwise a new file will be created. Then the combined file will be written in the output path.
I have written 5 folder for 5 cryptocurrencies using loop.
<img width="739" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/baca4c7d-3da1-457d-93f8-f7dfbec2800e">
<img width="929" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/cd2f4c78-b6aa-4acd-bf33-1e9e673d67a3">
(***aggregated data for binance coin***)


### Visualization:
I have used spark SQL to visualize the data and add them to particular dashboards for each coin.Here is an example
<img width="960" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/876a5548-d0a4-4eca-bdc2-c5dfadf33b4d">

## Other components:
### Sending message:
I have created an web activity to send mail for each successful pipeline runs.This web activity will send a post request to azure logic app with following body
<img width="960" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/ffc3e94a-4662-4f78-b173-415f2228bed6">

This will trigger the logic app to send mail to recipient.
<img width="926" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/61247a8b-03aa-4e5d-8133-c585577d395d">

### Auto-terminate cluster:
As the databricks cluster auto-terminated after 10 mins of inactivity, I want to save cost by immediately terminating the cluster after finishing the etl process.
<img width="912" alt="image" src="https://github.com/Aritra469/de_project1_synapse/assets/171404393/e8a884ef-c991-4d8f-acd7-3041b6433881">
First I get the databricks access token from the keyvault using webactivity and then set the activity output as a pipeline variable, then I used the pipeline variable for authorization and send a post request for databricks cluster termination.

1. ~~Have to automate the cluster termination process.~~
2. Have to collect pipeline success or error message and visualize using serverless sql.
3. Have to move previous months raw data in archive in yyyy/mm/dd or yyyy/mm structure.
