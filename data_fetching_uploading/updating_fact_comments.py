from google.oauth2 import service_account
from google.cloud import bigquery
import sys
import json
# Set up credentials and initialize the BigQuery client
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ['https://www.googleapis.com/auth/bigquery']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
bigquery_client = bigquery.Client(credentials=creds)

# Define the dataset and table IDs
config_path = "config.json"
with open(config_path, 'r') as file:
    config = json.load(file)
dataset_id = config.get('dataset_id')
fact_comment_table = "Fact_Comments"
staging_raw_table = "staging_raw_table"

# Set the variable for upload time from command line or default
default_upload_time = '2024-04-14'
upload_time = sys.argv[1] if len(sys.argv) > 1 else default_upload_time
merge_fact_comment = f"""
  MERGE INTO `{dataset_id}.{fact_comment_table}` AS destination
  USING (
      SELECT 
          comment_id,
          MAX(comment_text) AS comment_text,
          MAX(comment_score) AS comment_score,
          MAX(comment_date) AS comment_date,
          MAX(comment_user_id) AS comment_user_id
      FROM (
          SELECT 
              Comment_ID as comment_id,
              Comment_Text as comment_text,
              Comment_Score as comment_score,
              Comment_Date as comment_date,
              Comment_User_ID as comment_user_id
          FROM `{dataset_id}.{staging_raw_table}`
          WHERE upload_time = @upload_time
      )
      WHERE comment_id IS NOT NULL  -- Ensure that comment_id is not null
      GROUP BY comment_id
  ) AS source
  ON destination.comment_id = source.comment_id
  WHEN NOT MATCHED THEN
    INSERT (
      comment_id,
      comment_text,
      comment_score,
      comment_date,
      comment_user_id
    )
    VALUES (
      source.comment_id,
      source.comment_text,
      source.comment_score,
      source.comment_date,
      source.comment_user_id
    )
  WHEN MATCHED THEN
    UPDATE SET 
      comment_text = source.comment_text,
      comment_score = source.comment_score,
      comment_date = source.comment_date,
      comment_user_id = source.comment_user_id
"""
# Execute the merge query with query parameters
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP", upload_time),
    ]
)

# Run the query and ensure it completes
query_job = bigquery_client.query(merge_fact_comment, job_config=job_config)
query_job.result()  # Wait for the query to finish

print("Fact_Comment merge operation completed successfully.")




# Merge script to update the Fact_Comment table with unique Comment_ID's
# merge_fact_comment = f"""
# MERGE INTO `{dataset_id}.{fact_comment_table}` AS destination
# USING (
#     -- Ensure unique Comment_ID's by selecting the latest record
#     SELECT 
#         comment_id,
#         MAX(comment_text) AS comment_text,
#         MAX(comment_score) AS comment_score,
#         MAX(comment_date) AS comment_date,
#         MAX(comment_user_id) AS comment_user_id
#     FROM (
#         SELECT 
#             Comment_ID as comment_id,
#             Comment_Text as comment_text,
#             Comment_Score as comment_score,
#             Comment_Date as comment_date,
#             Comment_User_ID as comment_user_id
#         FROM `{dataset_id}.{staging_raw_table}`
#         WHERE upload_time = @upload_time
#     )
#     GROUP BY comment_id  # Ensure only unique Comment_ID's
# ) AS source
# ON destination.comment_id = source.comment_id
# WHEN NOT MATCHED THEN
#   INSERT (
#     comment_id,
#     comment_text,
#     comment_score,
#     comment_date,
#     comment_user_id
#   )
#   VALUES (
#     source.comment_id,
#     source.comment_text,
#     source.comment_score,
#     source.comment_date,
#     source.comment_user_id
#   )
# WHEN MATCHED THEN
#   UPDATE SET 
#     comment_text = source.comment_text,
#     comment_score = source.comment_score,
#     comment_date = source.comment_date,
#     comment_user_id = source.comment_user_id
# """