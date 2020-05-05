from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

table_id = "slackbot-260723.jobs.listings"

schema = [
    bigquery.SchemaField("Company", "STRING"),
    bigquery.SchemaField("CompanyURL", "STRING"),
    bigquery.SchemaField("Location", "STRING"),
    bigquery.SchemaField("Title", "STRING"),
    bigquery.SchemaField("HowToApply", "STRING"),
    bigquery.SchemaField("URL", "STRING"),
    bigquery.SchemaField("JobType", "STRING"),
    bigquery.SchemaField("Source", "STRING"),
    bigquery.SchemaField("Created", "TIMESTAMP"),
    bigquery.SchemaField("InsertDate", "TIMESTAMP"),
    bigquery.SchemaField("Data", "STRING"),
]

table = bigquery.Table(table_id, schema=schema)
table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="InsertDate",  # name of column to use for partitioning
) 
table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)