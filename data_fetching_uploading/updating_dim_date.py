from google.oauth2 import service_account
from google.cloud import bigquery
import sys
import json
# Set up the BigQuery client with service account credentials
SERVICE_ACCOUNT_FILE = "service_account.json"  # Adjust to your service account file
SCOPES = ['https://www.googleapis.com/auth/bigquery']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
bigquery_client = bigquery.Client(credentials=creds)

# Define BigQuery project, dataset, and table details
config_path = "config.json"
with open(config_path, 'r') as file:
    config = json.load(file)
dataset_id = config.get('dataset_id')  # Adjust to your dataset ID
table_name = "Dim_Date"  # Adjust to your target table name
default_upload_time = '2024-04-14'  # Default value for parameter
upload_time = sys.argv[1] if len(sys.argv) > 1 else default_upload_time  # Read from command line or use default

# Define the SQL script with parameterization
merge_sql = f"""
MERGE INTO `{dataset_id}.{table_name}` AS target
USING (
  SELECT
    d AS full_date,
    EXTRACT(YEAR FROM d) AS year,
    EXTRACT(WEEK FROM d) AS year_week,
    EXTRACT(DAY FROM d) AS year_day,
    EXTRACT(YEAR FROM d) AS fiscal_year,
    FORMAT_DATE('%Q', d) as fiscal_qtr,
    EXTRACT(MONTH FROM d) AS month,
    FORMAT_DATE('%B', d) as month_name,
    EXTRACT(DAYOFWEEK FROM d) AS week_day,
    FORMAT_DATE('%A', d) as day_name,
    (CASE WHEN EXTRACT(DAYOFWEEK FROM d) IN (1, 7) THEN 0 ELSE 1 END) AS day_is_weekday
  FROM
    UNNEST(GENERATE_DATE_ARRAY('2024-01-01', @upload_time, INTERVAL 1 DAY)) AS d
) AS source
ON target.full_date = source.full_date
WHEN MATCHED THEN
  UPDATE SET
    target.year = source.year,
    target.year_week = source.year_week,
    target.year_day = source.year_day,
    target.fiscal_year = source.fiscal_year,
    target.fiscal_qtr = source.fiscal_qtr,
    target.month = source.month,
    target.month_name = source.month_name,
    target.week_day = source.week_day,
    target.day_name = source.day_name,
    target.day_is_weekday = source.day_is_weekday
WHEN NOT MATCHED THEN
  INSERT (
    full_date,
    year,
    year_week,
    year_day,
    fiscal_year,
    fiscal_qtr,
    month,
    month_name,
    week_day,
    day_name,
    day_is_weekday
  )
  VALUES (
    source.full_date,
    source.year,
    source.year_week,
    source.year_day,
    source.fiscal_year,
    source.fiscal_qtr,
    source.month,
    source.month_name,
    source.week_day,
    source.day_name,
    source.day_is_weekday
  );
"""

# Create a QueryJobConfig with parameterization
query_config = bigquery.QueryJobConfig(
    query_parameters=[bigquery.ScalarQueryParameter("upload_time", "DATE", upload_time)]
)

# Execute the SQL script with the query configuration in BigQuery
query_job = bigquery_client.query(merge_sql, job_config=query_config)
query_job.result()  # Wait for the query to complete

print(f"Data merged into `{dataset_id}.{table_name}` successfully.")
