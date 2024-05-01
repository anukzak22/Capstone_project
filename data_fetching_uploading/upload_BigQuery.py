import sys
import pandas as pd
import datetime
from google.cloud import bigquery
from googleapiclient.discovery import build
from google.api_core.exceptions import NotFound
import io
from google.oauth2 import service_account
import json


# Function to calculate the start and end dates of the week
def get_week_boundaries(date):
    start_of_week = date - datetime.timedelta(days=date.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    return start_of_week, end_of_week

def get_last_file_id(filepath):
    df = pd.read_csv(filepath, delimiter=":", header=None, names=["Timestamp", "File_ID"], engine='python')
    last_row = df.iloc[-1]  # Get the last row
    last_file_id = last_row["File_ID"].strip()  # Extract the Google Drive file ID
    return last_file_id

# Function to create a BigQuery table if it doesn't exist
def create_bigquery_table(bigquery_client, dataset_id, table_name, schema=None):
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_name)

    # try:
    #     bigquery_client.get_table(table_ref)  # Check if the table exists
    #     print(f"Table {table_name} already exists in dataset {dataset_id}.")

    # except NotFound:
    #     if schema is None:
    #         schema = []  # Default schema allows autodetection
    #     table = bigquery.Table(table_ref, schema=schema)
    #     bigquery_client.create_table(table)  # Create the table
    #     print(f"Created table {table_name} in dataset {dataset_id}.")
    try:
        # If the table exists, delete it
        bigquery_client.get_table(table_ref)
        print(f"Table {table_name} exists in dataset {dataset_id}. Deleting it.")
        bigquery_client.delete_table(table_ref)  # Delete the existing table
        print(f"Deleted table {table_name}.")
    except NotFound:
        # If the table does not exist, just create a new one
        print(f"Table {table_name} does not exist in dataset {dataset_id}. Creating a new one.")

    # Create a new table with the specified schema
    if schema is None:
        schema = []  # Default schema allows autodetection
    table = bigquery.Table(table_ref, schema=schema)
    bigquery_client.create_table(table)
    print(f"Created table {table_name} in dataset {dataset_id}.")


# Function to load a CSV file from Google Drive into BigQuery
def load_csv_to_bigquery(drive_file_id, bigquery_dataset, bigquery_table_name, creds):
    # Google Drive service initialization
    drive_service = build('drive', 'v3', credentials=creds)

    # Download the CSV file from Google Drive
    request = drive_service.files().get_media(fileId=drive_file_id)
    file_data = io.BytesIO(request.execute())  # Load file into memory

    # Read the CSV into a DataFrame
    df = pd.read_csv(file_data)

    # Initialize the BigQuery client
    bigquery_client = bigquery.Client(credentials=creds)

    # Create the BigQuery table if it doesn't exist
    create_bigquery_table(bigquery_client, bigquery_dataset, bigquery_table_name)

    # Load the DataFrame into BigQuery
    table_ref = bigquery_client.dataset(bigquery_dataset).table(bigquery_table_name)
    custom_schema= [
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
        bigquery.SchemaField("Comment_User_Downvotes", "INTEGER", mode="NULLABLE")
    ]
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        allow_jagged_rows=True,
        max_bad_records=10,
        ignore_unknown_values=True,
        source_format=bigquery.SourceFormat.CSV,
        # autodetect=True,
        schema=custom_schema
    )

    load_job = bigquery_client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    load_job.result()  # Wait for completion

    print(f"Data loaded into BigQuery table: {bigquery_dataset}.{bigquery_table_name}")

def convert_string_to_timestamp(dataset_id, table_name, column_name,creds):

    bigquery_client = bigquery.Client(credentials=creds)
    # Define a SQL query to convert the column to TIMESTAMP
    convert_query = f"""
        CREATE OR REPLACE TABLE `{dataset_id}.{table_name}`
        AS
        SELECT *,
        TIMESTAMP({column_name}) AS {column_name}_timestamp  # Convert the specific column
        FROM `{dataset_id}.{table_name}`
    """

    # Execute the query
    query_job = bigquery_client.query(convert_query)
    query_job.result()  # Wait for the query to complete
    print(f"Converted column '{column_name}' to TIMESTAMP in table: {dataset_id}.{table_name}")


# Main script execution
if __name__ == "__main__":
    # Check if enough arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python new.py <date> <number>")
        sys.exit(1)

    # Get the command-line arguments
    date_str = sys.argv[1]  # The first argument is the date
    number = sys.argv[2]  # The second argument is the number

    # Parse the date
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    # Calculate the week boundaries
    start_of_week, end_of_week = get_week_boundaries(date)
    week_start_str = start_of_week.strftime("%Y-%m-%d")
    week_end_str = end_of_week.strftime("%Y-%m-%d")

    # Define the BigQuery table name
    bigquery_table_name = f"staged_table_{week_start_str}_{week_end_str}_{number}"
    print(bigquery_table_name)

    # Google Drive and BigQuery setup
    SERVICE_ACCOUNT_FILE = "service_account.json"  # Service account JSON key file
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/bigquery']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Path to the file with Google Drive file ID
    file_path = "file_id.txt"

    # Get the last Google Drive file ID
    last_file_id = get_last_file_id(file_path)
    print(last_file_id)

    # Load CSV into BigQuery with the dynamically created table name
    config_path = "config.json"
    with open(config_path, 'r') as file:
        config = json.load(file)
    dataset_id = config.get('dataset_id')  # BigQuery dataset
    load_csv_to_bigquery(last_file_id, dataset_id, bigquery_table_name, creds)
    column_to_convert_1 = "Post Date"
    column_to_convert_2 = "Comment Date"
    print("Uploaded the data")
    # convert_string_to_timestamp(bigquery_dataset, bigquery_table_name, column_to_convert_1,creds)
    # convert_string_to_timestamp(bigquery_dataset, bigquery_table_name, column_to_convert_2,creds)

