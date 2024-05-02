from google.cloud import bigquery
from google.oauth2 import service_account
import json

# Define your service account file path and scopes
SERVICE_ACCOUNT_FILE = "service_account.json"  # Adjust to your service account file
SCOPES = ['https://www.googleapis.com/auth/bigquery']

# Load credentials from service account file
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Create a BigQuery client with the credentials
bigquery_client = bigquery.Client(credentials=creds)

config_file_path = 'config.json'
# Read the current content of the JSON file
with open(config_file_path, 'r') as f:
    config = json.load(f)
dataset_id = config.get('dataset_id')  # Change to the desired dataset name

# Create the dataset reference
dataset_ref = bigquery_client.dataset(dataset_id)

# Define the dataset object with optional location setting (e.g., 'US')
dataset = bigquery.Dataset(dataset_ref)

# Set dataset properties (optional)
dataset.location = "US"  # You can change it to another location as needed

# Create the dataset in BigQuery
dataset = bigquery_client.create_dataset(dataset)  # This creates the dataset

print(f"Dataset '{dataset_id}' created in location '{dataset.location}'.")
