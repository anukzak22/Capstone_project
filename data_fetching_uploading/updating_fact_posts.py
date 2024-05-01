from google.oauth2 import service_account
from google.cloud import bigquery
import sys

# Set up credentials and initialize the BigQuery client
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ['https://www.googleapis.com/auth/bigquery']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
bigquery_client = bigquery.Client(credentials=creds)

# Define the dataset and table IDs
dataset_id = "stackoverflow_db"
fact_post_table = "Fact_Posts"
staging_raw_table = "staging_raw_table"

# Set the variable for upload time from command line or default
default_upload_time = '2024-04-14'
upload_time = sys.argv[1] if len(sys.argv) > 1 else default_upload_time

# Merge script to update the Fact_Post table with unique post_id's
merge_fact_post = f"""
MERGE INTO `{dataset_id}.{fact_post_table}` AS destination
USING (
    -- Ensure unique post_id's by selecting the latest record
    SELECT 
        post_id,
        MAX(post_date) AS post_date,
        MAX(title) AS title,
        MAX(body) AS body,
        MAX(user_id) AS user_id,
        MAX(score) AS score,
        MAX(view_count) AS view_count
    FROM (
        SELECT 
            Post_ID as post_id,
            Post_Date as post_date,
            Post_Title as title,
            Post_Body as body,
            Post_User_ID as user_id,
            Post_Score as score,
            Post_View_Count as view_count
        FROM `{dataset_id}.{staging_raw_table}`
        WHERE upload_time = @upload_time
    )
    GROUP BY post_id
) AS source
ON destination.post_id = source.post_id
WHEN NOT MATCHED THEN
  INSERT (
    post_id,
    post_date,
    title,
    body,
    user_id,
    score,
    view_count
  )
  VALUES (
    source.post_id,
    source.post_date,
    source.title,
    source.body,
    source.user_id,
    source.score,
    source.view_count
  )
WHEN MATCHED THEN
  UPDATE SET 
    post_date = source.post_date,
    title = source.title,
    body = source.body,
    user_id = source.user_id,
    score = source.score,
    view_count = source.view_count
"""

# Execute the merge query with query parameters
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP", upload_time),
    ]
)

# Run the query and ensure it completes
query_job = bigquery_client.query(merge_fact_post, job_config=job_config)
query_job.result()  # Wait for the query to finish

print("Fact_Post merge operation completed successfully.")





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
# fact_post_table = "fact_post"
# staging_raw_table = "staging_raw_table"

# # Set the variable for upload time from command line or default
# default_upload_time = '2024-04-14'
# upload_time = sys.argv[1] if len(sys.argv) > 1 else default_upload_time

# # Merge script to update the Fact_Post table
# merge_fact_post = f"""
# MERGE INTO `{dataset_id}.{fact_post_table}` AS destination
# USING (
#     SELECT 
#         Post_ID as post_id,
#         Post_Date as post_date,
#         Post_Title as title,
#         Post_Body as body,
#         Post_User_ID as user_id,
#         Post_Score as score,
#         Post_View_Count as view_count
#     FROM `{dataset_id}.{staging_raw_table}`
#     WHERE upload_time = @upload_time
# ) AS source
# ON destination.post_id = source.post_id
# WHEN NOT MATCHED THEN
#   INSERT (
#     post_id,
#     post_date,
#     title,
#     body,
#     user_id,
#     score,
#     view_count
#   )
#   VALUES (
#     source.post_id,
#     source.post_date,
#     source.title,
#     source.body,
#     source.user_id,
#     source.score,
#     source.view_count
#   )
# WHEN MATCHED THEN
#   UPDATE SET 
#     post_date = source.post_date,
#     title = source.title,
#     body = source.body,
#     user_id = source.user_id,
#     score = source.score,
#     view_count = source.view_count
# """
  
# # Execute the merge query with query parameters
# job_config = bigquery.QueryJobConfig(
#     query_parameters=[
#         bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP", upload_time),
#     ]
# )

# # Run the query and ensure it completes
# query_job = bigquery_client.query(merge_fact_post, job_config=job_config)
# query_job.result()  # Wait for the query to finish

# print("Fact_Post merge operation completed successfully.")