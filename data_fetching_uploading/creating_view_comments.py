import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import os
import sys
import json

# Google Cloud setup
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ['https://www.googleapis.com/auth/bigquery']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# BigQuery client and project details
bigquery_client = bigquery.Client(credentials=creds)
config_path = "config.json"
with open(config_path, 'r') as file:
    config = json.load(file)
dataset_id = config.get('dataset_id')
view_name = 'view_comments'

# Get the upload_time argument from command line
upload_time = sys.argv[1] if len(sys.argv) > 1 else None

if not upload_time:
    print("Error: No upload_time argument provided.")
    sys.exit(1)

# SQL query to create the BigQuery view for comments with associated post tags and upload_time
create_view_query = f"""
CREATE OR REPLACE VIEW `{dataset_id}.{view_name}` AS
SELECT
    fc.comment_id,
    fc.comment_text,
    fc.comment_score,
    pt.tag AS post_tag,  -- Tag from the bridge table
    sr.upload_time  -- Include upload_time from staging_raw_table
FROM
    `{dataset_id}.Fact_Comments` AS fc
LEFT JOIN
    `{dataset_id}.Bridge_Posts_Comments` AS bpc  -- Join to get post_id for each comment
    ON fc.comment_id = bpc.comment_id
LEFT JOIN
    `{dataset_id}.Bridge_Posts_Tags` AS pt  -- Join to get tags for each post
    ON bpc.post_id = pt.post_id
LEFT JOIN
    `{dataset_id}.staging_raw_table` AS sr  -- Join to get upload_time
    ON bpc.post_id = sr.Post_ID
WHERE
    sr.upload_time = TIMESTAMP('{upload_time}')  -- Filter by upload_time
"""

# Execute the SQL query to create the new view
bigquery_client.query(create_view_query)
print(f"Created new view for comments with post tags and upload_time='{upload_time}'.")

# Query to get the view result
query = f"SELECT * FROM `{dataset_id}.{view_name}`"

# Execute the query and load results into a Pandas DataFrame
dataframe = bigquery_client.query(query).to_dataframe()

# Save the DataFrame to a CSV file
csv_file_path = f'view_comments_{upload_time}.csv'  # File path for the CSV file
dataframe.to_csv(csv_file_path, index=False)  # Save without index

print(f"Data saved to CSV at {csv_file_path}")
