import pandas as pd
import sys
from google.cloud import bigquery
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import json
# Google Cloud and Google Drive setup
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ['https://www.googleapis.com/auth/bigquery', 'https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# BigQuery client and project details
bigquery_client = bigquery.Client(credentials=creds)
config_path = "config.json"
with open(config_path, 'r') as file:
    config = json.load(file)
dataset_id = config.get('dataset_id')
view_name = 'view_posts'

# Get the upload_time argument from command line
upload_time = sys.argv[1] if len(sys.argv) > 1 else None

if not upload_time:
    print("Error: No upload_time argument provided.")
    sys.exit(1)


# SQL query to create the BigQuery view with a WHERE clause for upload_time
create_view_query = f"""
CREATE OR REPLACE VIEW `{dataset_id}.{view_name}` AS
SELECT
    fp.post_id,
    fp.title AS post_title,
    fp.body AS post_body,
    fp.post_date,
    pt.tag  -- One row for each tag
FROM
    `{dataset_id}.Fact_Posts` AS fp
LEFT JOIN
    `{dataset_id}.Bridge_Posts_Tags` AS pt  -- Joining with bridge table for unique tags
    ON fp.post_id = pt.post_id
LEFT JOIN
    `{dataset_id}.staging_raw_table` AS sr  -- To get upload_time
    ON fp.post_id = sr.Post_ID
WHERE
    sr.upload_time = TIMESTAMP('{upload_time}')
"""

# Execute the SQL query to create the new view
bigquery_client.query(create_view_query)
print(f"Created new view for posts with upload_time='{upload_time}'.")

# Query to get the view result
query = f"SELECT * FROM `{dataset_id}.{view_name}`"

# Execute the query and load results into a Pandas DataFrame
dataframe = bigquery_client.query(query).to_dataframe()

# Get the total number of rows in the DataFrame
total_rows = len(dataframe)
print(f"Total number of rows: {total_rows}")

# Save the DataFrame to a CSV file
csv_file_path = f'view_posts_{upload_time}.csv'  # File path for the CSV file
dataframe.to_csv(csv_file_path, index=False)  # Save without DataFrame indices

print(f"Data saved to CSV at {csv_file_path}")
