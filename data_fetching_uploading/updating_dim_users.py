# from google.cloud import bigquery
# from google.oauth2 import service_account
# # Initialize a BigQuery client
# SERVICE_ACCOUNT_FILE = "service_account.json"
# SCOPES = ['https://www.googleapis.com/auth/bigquery']
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# bigquery_client = bigquery.Client(credentials=creds)
# # Define the dataset ID
# dataset_id = "stackoverflow_db"

# # Define the SQL query to merge into Dim_Users
# merge_dim_users = f"""
# MERGE INTO `{dataset_id}.dim_user` AS destination
# USING (
#     SELECT 
#         COALESCE(Post_User_ID, Comment_User_ID) AS user_id,
#         COALESCE(Post_User_Reputation, Comment_User_Reputation) AS reputation,
#         COALESCE(Post_User_Location, Comment_User_Location) AS location,
#         COALESCE(Post_User_Views, Comment_User_Views) AS views,
#         COALESCE(Post_User_Upvotes, Comment_User_Upvotes) AS up_votes,
#         COALESCE(Post_User_Downvotes, Comment_User_Downvotes) AS down_votes
#     FROM `{dataset_id}.staging_raw_table`
#     WHERE upload_time = '2024-04-07'
# ) AS source
# ON destination.user_id = source.user_id
# WHEN NOT MATCHED THEN
#   INSERT (user_id, reputation, views, up_votes, down_votes,location)
#   VALUES (
#     source.user_id, 
#     source.reputation, 
#     source.views, 
#     source.up_votes, 
#     source.down_votes,
#     source.location
#   )
# WHEN MATCHED AND (
#   destination.reputation != source.reputation OR
#   destination.views != source.views OR
#   destination.up_votes != source.up_votes OR
#   destination.down_votes != source.down_votes OR
#   destination.location != source.location 
# ) THEN
#   UPDATE SET 
#     reputation = source.reputation,
#     views = source.views,
#     up_votes = source.up_votes,
#     down_votes = source.down_votes,
#     location = source.location;
# """

# # Run the query
# query_job = bigquery_client.query(merge_dim_users)
# query_job.result()  # Waits for the query to finish

# print("Dim_Users merge operation completed successfully.")
# from google.cloud import bigquery
# from google.oauth2 import service_account

# # Set up credentials and initialize the BigQuery client
# SERVICE_ACCOUNT_FILE = "service_account.json"
# SCOPES = ['https://www.googleapis.com/auth/bigquery']
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# bigquery_client = bigquery.Client(credentials=creds)

# # Define the dataset and table IDs
# dataset_id = "stackoverflow_db"
# table_name = "Dim_Users"

# # Merge script to avoid duplicate user_id insertions
# merge_dim_user = f"""
# MERGE INTO `{dataset_id}.{table_name}` AS destination
# USING (
#     SELECT 
#         COALESCE(Post_User_ID, Comment_User_ID) AS user_id,
#         MAX(COALESCE(Post_User_Reputation, Comment_User_Reputation)) AS reputation,
#         MAX(COALESCE(Post_User_Location, Comment_User_Location)) AS location,
#         MAX(COALESCE(Post_User_Views, Comment_User_Views)) AS views,
#         MAX(COALESCE(Post_User_Upvotes, Comment_User_Upvotes)) AS up_votes,
#         MAX(COALESCE(Post_User_Downvotes, Comment_User_Downvotes)) AS down_votes
#     FROM `{dataset_id}.staging_raw_table`
#     WHERE upload_time = @upload_time
#     GROUP BY user_id
# ) AS source
# ON destination.user_id = source.user_id
# WHEN NOT MATCHED THEN
#   INSERT (user_id, reputation, location, views, up_votes, down_votes)
#   VALUES (
#     source.user_id, 
#     source.reputation, 
#     source.location, 
#     source.views, 
#     source.up_votes, 
#     source.down_votes
#   )
# WHEN MATCHED AND (
#   destination.reputation != source.reputation OR
#   destination.location != source.location OR
#   destination.views != source.views OR
#   destination.up_votes != source.up_votes OR
#   destination.down_votes != source.down_votes
# ) THEN
#   UPDATE SET 
#     reputation = source.reputation,
#     location = source.location,
#     views = source.views,
#     up_votes = source.up_votes,
#     down_votes = source.down_votes;
# """

# # Set the variable for upload time
# upload_time = '2024-04-07'  # Change this to your desired upload time

# # Execute the merge query
# job_config = bigquery.QueryJobConfig(
#     query_parameters=[
#         bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP", upload_time),
#     ]
# )
# query_job = bigquery_client.query(merge_dim_user, job_config=job_config)

# # Wait for the query to finish
# query_job.result()  # Ensures the query completes before continuing

# print("Dim_User merge operation completed successfully.")
# max_surrogate_key_query = f"""
# SELECT IFNULL(MAX(surrogate_key), 0) AS max_key
# FROM `{dataset_id}.{table_name}`
# """

# # Get the maximum key value
# max_surrogate_key_result = bigquery_client.query(max_surrogate_key_query).result()
# max_surrogate_key = list(max_surrogate_key_result)[0]['max_key']

# # Merge script to insert with auto-incrementing surrogate key
# merge_dim_user = f"""
# MERGE INTO `{dataset_id}.{table_name}` AS destination
# USING (
#     SELECT 
#         COALESCE(Post_User_ID, Comment_User_ID) AS user_id,
#         MAX(COALESCE(Post_User_Reputation, Comment_User_Reputation)) AS reputation,
#         MAX(COALESCE(Post_User_Location, Comment_User_Location)) AS location,
#         MAX(COALESCE(Post_User_Views, Comment_User_Views)) AS views,
#         MAX(COALESCE(Post_User_Upvotes, Comment_User_Upvotes)) AS up_votes,
#         MAX(COALESCE(Post_User_Downvotes, Comment_User_Downvotes)) AS down_votes
#     FROM `{dataset_id}.staging_raw_table`
#     WHERE upload_time = @upload_time
#     GROUP BY user_id
# ) AS source
# ON destination.user_id = source.user_id
# WHEN NOT MATCHED THEN
#   INSERT (surrogate_key, user_id, reputation, location, views, up_votes, down_votes)
#   VALUES (
#     {max_surrogate_key + 1},  # Auto-incrementing surrogate key
#     source.user_id, 
#     source.reputation, 
#     source.location, 
#     source.views, 
#     source.up_votes, 
#     source.down_votes
#   )
# WHEN MATCHED AND (
#   destination.reputation != source.reputation OR
#   destination.location != source.location OR
#   destination.views != source.views OR
#   destination.up_votes != source.up_votes OR
#   destination.down_votes != source.down_votes
# ) THEN
#   UPDATE SET 
#     reputation = source.reputation,
#     location = source.location,
#     views = source.views,
#     up_votes = source.up_votes,
#     down_votes = source.down_votes;
# """

# # Set the variable for upload time
# upload_time = '2024-04-14'  # Change this to your desired upload time

# # Execute the merge query
# job_config = bigquery.QueryJobConfig(
#     query_parameters=[
#         bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP", upload_time),
#     ]
# )
# query_job = bigquery_client.query(merge_dim_user, job_config=job_config)

# # Wait for the query to finish
# query_job.result()  # Ensures the query completes before continuing

# print("Dim_User merge operation completed successfully.")
from google.oauth2 import service_account
from google.cloud import bigquery
import datetime
import sys
import json
# Set up credentials and initialize the BigQuery client


SERVICE_ACCOUNT_FILE = "service_account.json"
# SERVICE_ACCOUNT_FILE = "data_fetching_copy/service_account.json"
SCOPES = ['https://www.googleapis.com/auth/bigquery']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
bigquery_client = bigquery.Client(credentials=creds)

default_upload_time = '2024-04-14'
upload_time = sys.argv[1] if len(sys.argv) > 1 else default_upload_time

# Define the dataset and table IDs
config_path = "config.json"
with open(config_path, 'r') as file:
    config = json.load(file)
dataset_id = config.get('dataset_id')
table_name = "Dim_Users"

# Merge script to avoid duplicate user_id insertions
merge_dim_user = f"""
MERGE INTO `{dataset_id}.{table_name}` AS destination
USING (
    SELECT 
        COALESCE(Post_User_ID, Comment_User_ID) AS user_id,
        MAX(COALESCE(Post_User_Reputation, Comment_User_Reputation)) AS reputation,
        MAX(COALESCE(Post_User_Location, Comment_User_Location)) AS location,
        MAX(COALESCE(Post_User_Views, Comment_User_Views)) AS views,
        MAX(COALESCE(Post_User_Upvotes, Comment_User_Upvotes)) AS up_votes,
        MAX(COALESCE(Post_User_Downvotes, Comment_User_Downvotes)) AS down_votes
    FROM `{dataset_id}.staging_raw_table`
    WHERE upload_time = @upload_time
    GROUP BY user_id
) AS source
ON destination.user_id = source.user_id
WHEN NOT MATCHED THEN
  INSERT (user_id, reputation, location, views, up_votes, down_votes)
  VALUES (
    source.user_id, 
    source.reputation, 
    source.location, 
    source.views, 
    source.up_votes, 
    source.down_votes
  )
WHEN MATCHED AND (
  destination.reputation != source.reputation OR
  destination.location != source.location OR
  destination.views != source.views OR
  destination.up_votes != source.up_votes OR
  destination.down_votes != source.down_votes
) THEN
  UPDATE SET 
    reputation = source.reputation,
    location = source.location,
    views = source.views,
    up_votes = source.up_votes,
    down_votes = source.down_votes;
"""



# Execute the merge query
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP",upload_time),
    ]
)
query_job = bigquery_client.query(merge_dim_user, job_config=job_config)

# Wait for the query to finish
query_job.result()  # Ensures the query completes before continuing

print("Dim_User merge operation completed successfully.")
