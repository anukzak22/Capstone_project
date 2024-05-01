from google.oauth2 import service_account
from google.cloud import bigquery
import sys
import json

# Set up the BigQuery client with service account credentials
SERVICE_ACCOUNT_FILE = "service_account.json"  # Adjust to your service account file
SCOPES = ['https://www.googleapis.com/auth/bigquery']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
bigquery_client = bigquery.Client(credentials=creds)
config_path = "config.json"
with open(config_path, 'r') as file:
    config = json.load(file)
dataset_id = config.get('dataset_id')

# Define upload time, dataset, and table details
default_upload_time = '2024-04-14'  # Adjust as needed
upload_time = sys.argv[1] if len(sys.argv) > 1 else default_upload_time
bridge_post_comment_table_name = "Bridge_Posts_Comments"  # Bridge table name
staging_table_name = "staging_raw_table"  # Staging table name

# Define the MERGE query for updating the bridge table with post_id and comment_id
merge_bridge_post_comment = f"""
MERGE INTO `{dataset_id}.{bridge_post_comment_table_name}` AS destination
USING (
    SELECT 
        DISTINCT post_id,
        comment_id
    FROM 
        `{dataset_id}.{staging_table_name}`
    WHERE 
        upload_time = @upload_time
) AS source
ON destination.post_id = source.post_id AND destination.comment_id = source.comment_id
WHEN NOT MATCHED THEN
  INSERT (post_id, comment_id)
  VALUES (source.post_id, source.comment_id)
WHEN MATCHED THEN
  UPDATE SET 
    post_id = source.post_id,  -- You can update fields as needed
    comment_id = source.comment_id
"""

# Execute the MERGE query with parameterized upload time
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP", upload_time),
    ]
)

query_job = bigquery_client.query(merge_bridge_post_comment, job_config=job_config)
query_job.result()  # Wait for the query to complete

print("Merge operation completed successfully in Bridge_Post_Comment.")
