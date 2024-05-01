# from google.cloud import bigquery
# from google.oauth2 import service_account
# from google.api_core import exceptions
# import datetime
# import sys

# # Set up BigQuery client with service account credentials
# SERVICE_ACCOUNT_FILE = "service_account.json"  # Path to your service account JSON key
# SCOPES = ['https://www.googleapis.com/auth/bigquery']
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# bigquery_client = bigquery.Client(credentials=creds)


# # Check if a date argument is provided when running the script

# def get_week_boundaries(date=None):
#     if date is None:
#         date = datetime.date.today()
#     # Calculate the starting date of the week containing the provided/specified date (Monday)
#     start_of_week = date - datetime.timedelta(days=date.weekday())
#     # Calculate the ending date of the week containing the provided/specified date (Sunday)
#     end_of_week = start_of_week + datetime.timedelta(days=6)
#     return start_of_week, end_of_week

# if len(sys.argv) > 1:
#         specific_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
# else:
#     specific_date = None

#     # Get week boundaries


# # Calculate the week boundaries
# start_of_week, end_of_week = get_week_boundaries(specific_date)
# week_start_str = start_of_week.strftime("%Y-%m-%d")
# week_end_str = end_of_week.strftime("%Y-%m-%d")
# # creating the staging table names 

# # Calculate the week boundaries


# # Define the BigQuery table name
# staging_table_name_1 = f"staged_table_{week_start_str}_{week_end_str}_1"
# staging_table_name_2 = f"staged_table_{week_start_str}_{week_end_str}_2"
# print(staging_table_name_1)
# # Define the dataset and merge table reference
# dataset_ref = bigquery.DatasetReference(bigquery_client.project, 'stackoverflow_db')  # Your dataset
# merge_table_ref = bigquery.TableReference(dataset_ref, 'staging_raw_5')  # Merge table reference


# # Define the desired schema, including the 'upload_time' field
# schema = [
#     bigquery.SchemaField("Post_ID", "INTEGER", mode="REQUIRED"),  
#     bigquery.SchemaField("Post_Title", "STRING", mode="NULLABLE"), 
#     bigquery.SchemaField("Post_Body", "STRING", mode="NULLABLE"), 
#     bigquery.SchemaField("Post_Tags", "STRING", mode="NULLABLE"), 
#     bigquery.SchemaField("Post_Date", "TIMESTAMP", mode="NULLABLE"), 
#     bigquery.SchemaField("Post_Score", "INTEGER", mode="NULLABLE"), 
#     bigquery.SchemaField("Post_View_Count", "INTEGER", mode="NULLABLE"), 
#     bigquery.SchemaField("Answer_Count", "INTEGER", mode="NULLABLE"), 
#     bigquery.SchemaField("Comment_Count", "INTEGER", mode="NULLABLE"), 
    
#     bigquery.SchemaField("Post_User_ID", "INTEGER", mode="REQUIRED"),  
#     bigquery.SchemaField("Post_User_Reputation", "INTEGER", mode="NULLABLE"),  
#     bigquery.SchemaField("Post_User_Location", "STRING", mode="NULLABLE"),  
#     bigquery.SchemaField("Post_User_Views", "INTEGER", mode="NULLABLE"),  
#     bigquery.SchemaField("Post_User_Upvotes", "INTEGER", mode="NULLABLE"),  
#     bigquery.SchemaField("Post_User_Downvotes", "INTEGER", mode="NULLABLE"),  
    
#     bigquery.SchemaField("Comment_ID", "INTEGER", mode="NULLABLE"),  
#     bigquery.SchemaField("Comment_Text", "STRING", mode="NULLABLE"),  
#     bigquery.SchemaField("Comment_Score", "INTEGER", mode="NULLABLE"),  
#     bigquery.SchemaField("Comment_Date", "TIMESTAMP", mode="NULLABLE"),  
    
#     bigquery.SchemaField("Comment_User_ID", "INTEGER", mode="NULLABLE"),  
#     bigquery.SchemaField("Comment_User_Reputation", "INTEGER", mode="NULLABLE"),  
#     bigquery.SchemaField("Comment_User_Location", "STRING", mode="NULLABLE"),  
#     bigquery.SchemaField("Comment_User_Views", "INTEGER", mode="NULLABLE"),  
#     bigquery.SchemaField("Comment_User_Upvotes", "INTEGER", mode="NULLABLE"),  
#     bigquery.SchemaField("Comment_User_Downvotes", "INTEGER", mode="NULLABLE"),  
    
#     bigquery.SchemaField("upload_time", "TIMESTAMP", mode="NULLABLE")  
# ]

# # Check if the merge table exists, and create it if it doesn't
# try:
#     table = bigquery_client.get_table(merge_table_ref)  # Check if table exists
# except exceptions.NotFound:
#     # If not, create a new table with the specified schema
#     table = bigquery.Table(merge_table_ref, schema=schema)
#     bigquery_client.create_table(table)  # Create the table with the defined schema

# # Function to insert data from a staging table into the merge table with a specified upload time
# def insert_with_upload_time(source_table_ref, destination_table_ref, upload_time):
#     query = f"""
#         INSERT INTO `{destination_table_ref.project}.{destination_table_ref.dataset_id}.{destination_table_ref.table_id}`
#         SELECT *, TIMESTAMP("{upload_time.isoformat()}") AS upload_time
#         FROM `{source_table_ref.project}.{source_table_ref.dataset_id}.{source_table_ref.table_id}`
#     """
#     bigquery_client.query(query).result()  # Execute the query


# def drop_table(table_ref):
#     try:
#         bigquery_client.delete_table(table_ref)  # Delete the table
#         print(f"Deleted table: {table_ref.table_id}")
#     except exceptions.NotFound:
#         print(f"Table not found: {table_ref.table_id}")

# # Define the staging table references
# staging_table_ref1 = bigquery.TableReference(dataset_ref, staging_table_name_1)  # Staging table 1
# staging_table_ref2 = bigquery.TableReference(dataset_ref, staging_table_name_2)  # Staging table 2

# # Insert data from staging tables into the merge table with the specified upload time
# insert_with_upload_time(staging_table_ref1, merge_table_ref, specific_date)  # Insert data from staging table 1
# insert_with_upload_time(staging_table_ref2, merge_table_ref, specific_date)  # Insert data from staging table 2

# print(f"Data inserted into '{merge_table_ref.table_id}' with upload_time: {specific_date.isoformat()}")

# # Drop the staging tables after insertion
# drop_table(staging_table_ref1)  # Drop staging table 1
# drop_table(staging_table_ref2)

# print("Tables droped ")
import datetime
import sys
from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
from google.api_core import exceptions

# Set up the BigQuery client using a service account for authentication
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ['https://www.googleapis.com/auth/bigquery']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
bigquery_client = bigquery.Client(credentials=creds)

# Function to calculate the start and end of a given week
def get_week_boundaries(date=None):
    if date is None:
        date = datetime.date.today()  # If no date is provided, use today's date
    start_of_week = date - datetime.timedelta(days=date.weekday())  # Monday
    end_of_week = start_of_week + datetime.timedelta(days=6)  # Sunday
    return start_of_week, end_of_week

# Get the specific date from command-line arguments or use today's date
if len(sys.argv) > 1:
    specific_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
else:
    specific_date = datetime.date.today()

# Get week boundaries
start_of_week, end_of_week = get_week_boundaries(specific_date)
week_start_str = start_of_week.strftime("%Y-%m-%d")
week_end_str = end_of_week.strftime("%Y-%m-%d")

# Define dataset and table references for BigQuery
dataset_ref = bigquery.DatasetReference(bigquery_client.project, 'stackoverflow_db')
merge_table_ref = bigquery.TableReference(dataset_ref, 'staging_raw_table')

# Schema for the merge table
schema = [
    bigquery.SchemaField("unique_id", "INTEGER", mode="REQUIRED"),  # Unique identifier (surrogate key)s
    bigquery.SchemaField("upload_time", "TIMESTAMP", mode="REQUIRED"),  # Upload time
    bigquery.SchemaField("Post_ID", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("Post_Title", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Post_Body", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Post_Tags", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Post_Date", "TIMESTAMP", mode="NULLABLE"),
    bigquery.SchemaField("Post_Score", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Post_View_Count", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Answer_Count", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Comment_Count", "INTEGER", mode="NULLABLE"),
    
    bigquery.SchemaField("Post_User_ID", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("Post_User_Reputation", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Post_User_Location", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Post_User_Views", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Post_User_Upvotes", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Post_User_Downvotes", "INTEGER", mode="NULLABLE"),
    
    bigquery.SchemaField("Comment_ID", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Comment_Text", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Comment_Score", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Comment_Date", "TIMESTAMP", mode="NULLABLE"),
    
    bigquery.SchemaField("Comment_User_ID", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Comment_User_Reputation", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Comment_User_Location", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Comment_User_Views", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Comment_User_Upvotes", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Comment_User_Downvotes", "INTEGER", mode="NULLABLE"),
]

# Create the merge table if it doesn't exist
try:
    table = bigquery_client.get_table(merge_table_ref)  # Check if the table exists
except NotFound:
    table = bigquery.Table(merge_table_ref, schema=schema)  # Create it if it doesn't
    bigquery_client.create_table(table)


# Function to insert data with generated UUID as the unique identifier
def insert_with_autoincrement_id(source_table_ref, destination_table_ref, upload_time):
    query = f"""
    INSERT INTO `{destination_table_ref.project}.{destination_table_ref.dataset_id}.{destination_table_ref.table_id}`
    (unique_id, upload_time, Post_ID, Post_Title, Post_Body, Post_Tags, Post_Date, Post_Score, Post_View_Count, 
    Answer_Count, Comment_Count, Post_User_ID, Post_User_Reputation, Post_User_Location, Post_User_Views,
    Post_User_Upvotes, Post_User_Downvotes, Comment_ID, Comment_Text, Comment_Score, Comment_Date,
    Comment_User_ID, Comment_User_Reputation, Comment_User_Location, Comment_User_Views,
    Comment_User_Upvotes, Comment_User_Downvotes)
    SELECT 
    ROW_NUMBER() OVER (ORDER BY TIMESTAMP("{upload_time.isoformat()}")) + IFNULL((SELECT MAX(unique_id) FROM `{destination_table_ref.project}.{destination_table_ref.dataset_id}.{destination_table_ref.table_id}`), 0) AS unique_id,
    TIMESTAMP("{upload_time.isoformat()}") AS upload_time,
    Post_ID, Post_Title, Post_Body, Post_Tags, Post_Date, Post_Score, Post_View_Count,
    Answer_Count, Comment_Count, Post_User_ID, Post_User_Reputation, Post_User_Location,
    Post_User_Views, Post_User_Upvotes, Post_User_Downvotes, Comment_ID, Comment_Text, Comment_Score, Comment_Date,
    Comment_User_ID, Comment_User_Reputation, Comment_User_Location, Comment_User_Views,
    Comment_User_Upvotes, Comment_User_Downvotes
    FROM `{source_table_ref.project}.{source_table_ref.dataset_id}.{source_table_ref.table_id}`
"""
    bigquery_client.query(query).result()  # Execute the insert query

# Update calls to the function


# Define references for staging tables
staging_table_ref1 = bigquery.TableReference(dataset_ref, f"staged_table_{week_start_str}_{week_end_str}_1")
staging_table_ref2 = bigquery.TableReference(dataset_ref, f"staged_table_{week_start_str}_{week_end_str}_2")
insert_with_autoincrement_id(staging_table_ref1, merge_table_ref, specific_date)
insert_with_autoincrement_id(staging_table_ref2, merge_table_ref, specific_date)
# Insert data into merge table with generated UUIDs and unique starting key
# insert_with_uuids(staging_table_ref1, merge_table_ref, specific_date)
# insert_with_uuids(staging_table_ref2, merge_table_ref, specific_date)

# Output a success message with starting surrogate key
print(f"Data inserted into '{merge_table_ref.table_id}' with uuid key starting at.")

def drop_table(table_ref):
    try:
        bigquery_client.delete_table(table_ref)  # Delete the table
        print(f"Deleted table: {table_ref.table_id}")
    except exceptions.NotFound:
        print(f"Table not found: {table_ref.table_id}")

drop_table(staging_table_ref1)  # Drop staging table 1
drop_table(staging_table_ref2)