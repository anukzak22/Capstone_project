# from google.oauth2 import service_account
# from google.cloud import bigquery
# import sys

# # Set up credentials and initialize the BigQuery client
# SERVICE_ACCOUNT_FILE = "service_account.json"
# SCOPES = ['https://www.googleapis.com/auth/bigquery']
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# bigquery_client = bigquery.Client(credentials=creds)

# # Define the dataset and table IDs
# dataset_id = "stackoverflow_db"
# dim_tags_table = "Dim_Tags"
# staging_raw_table = "staging_raw_table"

# # Set the variable for upload time from command line or default
# default_upload_time = '2024-04-14'
# upload_time = sys.argv[1] if len(sys.argv) > 1 else default_upload_time

# # Corrected query to extract distinct tags
# split_tags_query = f"""
# WITH SplitTags AS (
#     -- Splitting and trimming tags into individual elements
#     SELECT 
#         TRIM(UNNEST(SPLIT(REPLACE(Post_Tags, '><', ','))), '<>') AS tag_name
#     FROM 
#         `{dataset_id}.{staging_raw_table}`
#     WHERE upload_time = @upload_time
# )

# SELECT DISTINCT 
#     tag_name
# FROM 
#     SplitTags
# """

# # Merge script for updating the dim_tags table
# merge_dim_tags = f"""
# MERGE INTO `{dataset_id}.{dim_tags_table}` AS destination
# USING ({split_tags_query}) AS source
# ON destination.tag_name = source.tag_name
# WHEN NOT MATCHED THEN
#   INSERT (tag_name) 
#   VALUES (source.tag_name)
# """

# # Execute the query with query parameters
# job_config = bigquery.QueryJobConfig(
#     query_parameters=[
#         bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP", upload_time),
#     ]
# )

# # Execute the query and wait for completion
# query_job = bigquery_client.query(merge_dim_tags, job_config=job_config)
# query_job.result()  # Wait for the query to finish

# print("dim_tags table updated successfully.")

from google.oauth2 import service_account
from google.cloud import bigquery
import sys
import json
# Set up the BigQuery client with service account credentials
SERVICE_ACCOUNT_FILE = "service_account.json"  # Adjust to your service account file
SCOPES = ['https://www.googleapis.com/auth/bigquery']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
bigquery_client = bigquery.Client(credentials=creds)

# Define upload time, dataset, and table details
default_upload_time = '2024-04-14'  # Adjust as needed
upload_time = sys.argv[1] if len(sys.argv) > 1 else default_upload_time
config_path = "config.json"
with open(config_path, 'r') as file:
    config = json.load(file)
dataset_id = config.get('dataset_id')  # Adjust to your dataset
staging_table_name = "staging_raw_table"  # Staging table name
dim_tags_table_name = "Dim_Tags"  # Destination table name

# Define the MERGE query with unique tags
merge_unique_tags = f"""
MERGE INTO `{dataset_id}.{dim_tags_table_name}` AS destination
USING (
    WITH SplitTags AS (
    -- Split the tags into individual rows
    SELECT 
        TRIM(tag_name, '<>') AS tag_name
    FROM 
        `{dataset_id}.{staging_table_name}`,
        UNNEST(SPLIT(REPLACE(post_tags, '><', ','), ',')) AS tag_name
    WHERE 
        upload_time = @upload_time
)
    SELECT 
        DISTINCT tag_name
    FROM 
        SplitTags
) AS source
ON destination.tag_name = source.tag_name
WHEN NOT MATCHED THEN
  INSERT (tag_name)
  VALUES (source.tag_name)
WHEN MATCHED THEN
  UPDATE SET 
    tag_name = source.tag_name
"""

# Execute the MERGE query with parameterized upload time
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP", upload_time),
    ]
)

query_job = bigquery_client.query(merge_unique_tags, job_config=job_config)
query_job.result()  # Wait for the query to complete

print("Unique tags merge operation completed successfully in Dim_Tags.")
