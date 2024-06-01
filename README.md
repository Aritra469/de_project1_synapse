# de_project1_synapse
Using api as source and spark pool to transform data
To ingest data from the Finnhub API into Azure Synapse Analytics, you can follow these steps:

1. **Set Up Azure Synapse Analytics Environment**:
   - Ensure you have an Azure Synapse workspace.
   - Create a dedicated SQL pool if you don't already have one.

2. **Obtain Finnhub API Key**:
   - Sign up on [Finnhub](https://finnhub.io/) to get your API key.

3. **Create a Linked Service in Azure Synapse**:
   - Go to your Azure Synapse workspace.
   - Under **Manage**, select **Linked services**.
   - Create a new linked service for the HTTP source (Finnhub API).

4. **Create a Data Flow in Synapse Studio**:
   - Navigate to the **Data** section and select **Data flows**.
   - Create a new data flow and add a source.

5. **Configure the Source to Use Finnhub API**:
   - Select the HTTP linked service you created.
   - Enter the Finnhub API endpoint (e.g., `https://finnhub.io/api/v1/stock/symbol?exchange=US&token=YOUR_API_KEY`).

6. **Parse the JSON Data**:
   - Add a transformation to parse the JSON response from the API.
   - Use the schema projection feature to map the JSON data to the desired columns.

7. **Write Data to Synapse**:
   - Add a sink transformation.
   - Choose the destination as your dedicated SQL pool.
   - Map the columns from the parsed JSON to the SQL table columns.

8. **Trigger the Data Flow**:
   - You can schedule this data flow to run at regular intervals using a Synapse pipeline.
   - Create a new pipeline, add a data flow activity, and configure it to run your data flow.

Here’s a step-by-step example for better clarity:

### Step-by-Step Example

#### 1. Set Up Azure Synapse Environment
1. Go to the Azure portal.
2. Create a new Azure Synapse Analytics workspace.
3. Create a dedicated SQL pool within the Synapse workspace.

#### 2. Obtain Finnhub API Key
1. Sign up on [Finnhub](https://finnhub.io/) to get an API key.
2. Keep the API key handy for later steps.

#### 3. Create a Linked Service
1. Go to your Synapse workspace.
2. Click on **Manage** > **Linked services**.
3. Click **+ New** and select **HTTP**.
4. Configure the HTTP linked service:
   - Base URL: `https://finnhub.io/api/v1`
   - Authentication type: Anonymous (if your API key is in the query string)
   - Add the API key to the query parameters or headers.

#### 4. Create a Data Flow
1. Navigate to the **Data** section.
2. Select **Data flows** and click **+ New data flow**.
3. Add a source transformation.

#### 5. Configure the Source
1. In the source transformation, choose the HTTP linked service you created.
2. Set the **Source options**:
   - HTTP method: GET
   - Relative URL: `/stock/symbol?exchange=US&token=YOUR_API_KEY`
3. Configure the response format (JSON).

#### 6. Parse JSON Data
1. Add a derived column transformation to parse the JSON response.
2. Use the built-in JSON functions to extract data fields.

#### 7. Write Data to Synapse
1. Add a sink transformation.
2. Select your dedicated SQL pool as the destination.
3. Map the columns from the JSON response to the SQL table columns.

#### 8. Schedule the Data Flow
1. Create a new pipeline.
2. Add a data flow activity and configure it to run the data flow.
3. Set up a trigger to schedule the pipeline execution (e.g., daily, hourly).

### Sample Pipeline Code (Using Azure Synapse Pipeline JSON)

Here’s an example of how the pipeline JSON might look:

```json
{
  "name": "IngestFinnhubData",
  "properties": {
    "activities": [
      {
        "name": "IngestData",
        "type": "DataFlow",
        "dependsOn": [],
        "policy": {
          "timeout": "7.00:00:00",
          "retry": 0,
          "retryIntervalInSeconds": 30,
          "secureOutput": false,
          "secureInput": false
        },
        "userProperties": [],
        "typeProperties": {
          "dataflow": {
            "referenceName": "FinnhubDataFlow",
            "type": "DataFlowReference"
          },
          "staging": {
            "linkedService": {
              "referenceName": "AzureBlobStorageLinkedService",
              "type": "LinkedServiceReference"
            },
            "folderPath": "staging"
          }
        }
      }
    ],
    "annotations": []
  }
}
```

This code is a template for an Azure Synapse pipeline that runs the data flow. Adjust it based on your specific configurations and requirements.

By following these steps, you can automate the ingestion of data from the Finnhub API into Azure Synapse Analytics for further analysis and reporting.

Problems faced:
the output of web activity exceeded 4mb limit so I have to use gzip in header.
