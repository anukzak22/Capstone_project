
# from google.oauth2 import service_account
# from google.cloud import bigquery
# import sys

# # Set up the BigQuery client with service account credentials
# SERVICE_ACCOUNT_FILE = "service_account.json"  # Adjust to your service account file
# SCOPES = ['https://www.googleapis.com/auth/bigquery']
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# bigquery_client = bigquery.Client(credentials=creds)

# # Define upload time, dataset, and table details
# default_upload_time = '2024-04-14'  # Adjust as needed
# upload_time = sys.argv[1] if len(sys.argv) > 1 else default_upload_time
# dataset_id = "stackoverflow_db"  # Adjust to your dataset
# bridge_table_name = "Bridge_Posts_Tags"  # Bridge table name
# staging_table_name = "staging_raw_table"  # Staging table name

# # Define the MERGE query to insert or update records in the bridge table
# merge_bridge_tags = f"""
# MERGE INTO `{dataset_id}.{bridge_table_name}` AS destination
# USING (
#     SELECT DISTINCT
#         post_id,
#         post_tags
#     FROM 
#         `{dataset_id}.{staging_table_name}`
#     WHERE 
#         upload_time = @upload_time
# ) AS source
# ON destination.post_id = source.post_id
# WHEN NOT MATCHED THEN
#   INSERT (post_id, post_tags)
#   VALUES (source.post_id, source.post_tags)
# WHEN MATCHED THEN
#   UPDATE SET 
#     post_tags = source.post_tags  -- Update tags when matched
# """

# # Execute the query with parameterized upload time
# job_config = bigquery.QueryJobConfig(
#     query_parameters=[
#         bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP", upload_time),
#     ]
# )

# query_job = bigquery_client.query(merge_bridge_tags, job_config=job_config)
# query_job.result()  # Wait for the query to complete

# print("Merge operation completed successfully in Bridge_Posts_Tags.")

# /////////////////////////


from google.oauth2 import service_account
from google.cloud import bigquery
import sys

# Set up the BigQuery client with service account credentials
SERVICE_ACCOUNT_FILE = "service_account.json"  # Adjust to your service account file
SCOPES = ['https://www.googleapis.com/auth/bigquery']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
bigquery_client = bigquery.Client(credentials=creds)

# Define upload time, dataset, and table details
default_upload_time = '2024-04-14'  # Adjust as needed
upload_time = sys.argv[1] if len(sys.argv) > 1 else default_upload_time
dataset_id = "stackoverflow_db"  # Adjust to your dataset
bridge_table_name = "Bridge_Posts_Tags"  # Bridge table name
staging_table_name = "staging_raw_table"  # Staging table name

# Define the MERGE query with split tags
merge_split_tags = f"""

MERGE INTO `{dataset_id}.{bridge_table_name}` AS destination
USING (
  WITH SplitTags AS (
    -- Split the tags into individual rows
    SELECT 
        post_id,
        TRIM(tag, '<>') AS tag,
        post_tags
    FROM 
        `{dataset_id}.{staging_table_name}`,
        UNNEST(SPLIT(REPLACE(post_tags, '><', ','), ',')) AS tag
    WHERE 
        upload_time = @upload_time
)
    SELECT 
        DISTINCT post_id,
        post_tags,
        tag
    FROM 
        SplitTags
) AS source
ON destination.post_id = source.post_id AND destination.post_tags = source.post_tags AND destination.tag = source.tag
WHEN NOT MATCHED THEN
  INSERT (post_id, post_tags, tag)
  VALUES (source.post_id, source.post_tags, source.tag)
WHEN MATCHED THEN
  UPDATE SET 
    post_tags = source.post_tags
"""

# Execute the MERGE query with parameterized upload time
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP", upload_time),
    ]
)

query_job = bigquery_client.query(merge_split_tags, job_config=job_config)
query_job.result()  # Wait for the query to complete

print("SplitTags merge operation completed successfully in Bridge_Posts_Tags.")
# # /////////////////////////////

# from google.oauth2 import service_account
# from google.cloud import bigquery
# import sys

# # Set up the BigQuery client with service account credentials
# SERVICE_ACCOUNT_FILE = "service_account.json"  # Adjust to your service account file
# SCOPES = ['https://www.googleapis.com/auth/bigquery']
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# bigquery_client = bigquery.Client(credentials=creds)

# # Define upload time, dataset, and table details
# default_upload_time = '2024-04-14'  # Adjust as needed
# upload_time = sys.argv[1] if len(sys.argv) > 1 else default_upload_time
# dataset_id = "stackoverflow_db"  # Adjust to your dataset
# bridge_table_name = "Bridge_Posts_Tags"  # Bridge table name
# staging_table_name = "staging_raw_table"  # Staging table name

# # Define the query that generates unique source rows
# split_tags_query = f"""
# WITH SplitTags AS (
#     -- Split the tags into individual rows
#     SELECT 
#         post_id,
#         TRIM(tag, '<>') AS tag,
#         post_tags
#     FROM 
#         `{dataset_id}.{staging_table_name}`,
#         UNNEST(SPLIT(REPLACE(post_tags, '><', ','), ',')) AS tag
#     WHERE 
#         upload_time = @upload_time
# )

# -- Ensure no duplicates with GROUP BY and aggregation
# SELECT 
#     post_id,
#     ARRAY_AGG(DISTINCT tag ORDER BY tag) AS unique_tags,
#     MAX(post_tags) AS original_post_tags  # Using MAX or any other aggregation to avoid duplicates
# FROM 
#     SplitTags
# GROUP BY 
#     post_id
# """

# # Corrected MERGE query for the bridge table
# merge_query = f"""
# MERGE INTO `{dataset_id}.{bridge_table_name}` AS destination
# USING (
#     SELECT 
#         post_id,
#         ARRAY_TO_STRING(unique_tags, ',') AS aggregated_tags,  # Convert array to string
#         original_post_tags
#     FROM 
#         ({split_tags_query})
# ) AS source
# ON 
#     destination.post_id = source.post_id
# WHEN NOT MATCHED THEN
#   INSERT (post_id, post_tags, tag)
#   VALUES (source.post_id, source.aggregated_tags, source.aggregated_tags)
# WHEN MATCHED THEN
#   UPDATE SET 
#     post_tags = source.aggregated_tags
# """

# # Execute the MERGE query with parameterized upload time
# job_config = bigquery.QueryJobConfig(
#     query_parameters=[
#         bigquery.ScalarQueryParameter("upload_time", "TIMESTAMP", upload_time),
#     ]
# )

# query_job = bigquery_client.query(merge_query, job_config=job_config)
# query_job.result()  # Wait for the query to complete

# print("Corrected merge operation completed successfully in Bridge_Posts_Tags.")
