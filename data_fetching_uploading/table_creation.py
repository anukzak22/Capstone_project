from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound

# Initialize a BigQuery client
# SERVICE_ACCOUNT_FILE = "data_fetching_copy/service_account.json"
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ['https://www.googleapis.com/auth/bigquery']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
bigquery_client = bigquery.Client(credentials=creds)


# List of table names to delete
tables_to_delete = [
    "Dim_Tags",
    "Dim_Date",
    "Bridge_Posts_Tags",
    "Fact_Posts",
    "Bridge_Posts_Comments",
    "Fact_Comments",
    "Dim_Users",
]

dataset_id = "stackoverflow_db"

# Create tables in the specified dataset
dataset_ref = bigquery_client.dataset(dataset_id)

# Loop through the tables to check and delete them if they exist
for table_name in tables_to_delete:
    table_ref = dataset_ref.table(table_name)  # Get the table reference
    try:
        # Check if the table exists before attempting to delete it
        bigquery_client.get_table(table_ref)  # This will raise an exception if the table doesn't exist
        bigquery_client.delete_table(table_ref)  # Delete the table
        print(f"Deleted table: {table_name}")
    except NotFound:
        print(f"Table {table_name} does not exist, skipping deletion.")
    except Exception as e:
        print(f"Failed to delete table {table_name}: {e}")


# Create DIM_TIME Table Schema
dim_date_schema = [
    bigquery.SchemaField("full_date", "DATE", mode="NULLABLE"),
    bigquery.SchemaField("year", "INTEGER", mode="NULLABLE"), 
    bigquery.SchemaField("year_week", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("year_day", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("fiscal_year", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("fiscal_qtr", "STRING", mode="NULLABLE"), # Primary key
    bigquery.SchemaField("month", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("month_name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("week_day", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("day_name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("day_is_weekday", "INTEGER", mode="NULLABLE"),
]

# Create DIM_USER Table Schema
dim_user_schema = [
    bigquery.SchemaField("unique_id", "INTEGER", mode="NULLABLE"),  # Surrogate key 
    bigquery.SchemaField("user_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("reputation", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("location", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("views", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("up_votes", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("down_votes", "INTEGER", mode="NULLABLE"),
    
]

# Create DIM_TAG Table Schema
dim_tag_schema = [
    bigquery.SchemaField("tag_id", "INTEGER", mode="NULLABLE"),  # Surrogate key 
    bigquery.SchemaField("tag_name", "STRING", mode="NULLABLE"),
]

# Create FACT_COMMENT Table Schema
fact_comment_schema = [
    bigquery.SchemaField("unique_id", "INTEGER", mode="NULLABLE"), # Surrogate key 
    bigquery.SchemaField("comment_id", "INTEGER", mode="REQUIRED"), 
    bigquery.SchemaField("comment_text", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("comment_date", "TIMESTAMP", mode="NULLABLE"),
    bigquery.SchemaField("comment_user_id", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("comment_score", "INTEGER", mode="NULLABLE"),
]

# Create FACT_POST Table Schema
fact_post_schema = [
    bigquery.SchemaField("unique_id", "INTEGER", mode="NULLABLE"),# Surrogate key 
    bigquery.SchemaField("post_id", "INTEGER", mode="REQUIRED"), 
    bigquery.SchemaField("post_date", "TIMESTAMP", mode="NULLABLE"),
    bigquery.SchemaField("title", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("body", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("user_id", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("score", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("view_count", "INTEGER", mode="NULLABLE"),
]

post_tags_schema = [
    bigquery.SchemaField("unique_id", "INTEGER", mode="NULLABLE"),# Surrogate key 
    bigquery.SchemaField("post_id", "INTEGER", mode="REQUIRED"),  
    bigquery.SchemaField("post_tags", "STRING", mode="NULLABLE"), 
    bigquery.SchemaField("tag", "STRING", mode="NULLABLE"),  
]

post_comment_schema = [
    bigquery.SchemaField("unique_id", "INTEGER", mode="NULLABLE"),# Surrogate key 
    bigquery.SchemaField("post_id", "INTEGER", mode="REQUIRED"),  
    bigquery.SchemaField("comment_id", "INTEGER", mode="NULLABLE"),
]

# Create Tables in BigQuery
tables_to_create = {
    "Dim_Date": dim_date_schema,
    "Bridge_Posts_Comments": post_comment_schema,
    "Dim_Tags": dim_tag_schema, 
    "Bridge_Posts_Tags": post_tags_schema,
    "Fact_Comments": fact_comment_schema,
    "Fact_Posts": fact_post_schema,
    "Dim_Users": dim_user_schema
}

for table_name, schema in tables_to_create.items():
    table_ref = dataset_ref.table(table_name)  # Table reference
    table = bigquery.Table(table_ref, schema=schema)  # Define the table
    try:
        # Create the table if it does not exist or recreate it if deleted
        bigquery_client.create_table(table, exists_ok=True)  
        print(f"Created table: {table_name}")
    except Exception as e:
        print(f"Error creating table {table_name}: {e}")