import os
import datetime
import sys
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import json
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "service_account.json"
# PARENT_FOLDER_ID = "1RHpeyvWOBZ-BtjrfQ6rNVTVTC1nBAH1g" 
config_path= "config.json"
with open(config_path, 'r') as file:
    config = json.load(file)
PARENT_FOLDER_ID = config.get("PARENT_FOLDER_ID", None) # ID of the parent folder change if you want to save in your own folder 
FOLDER_ID_FILE = "folder_id.txt"  # File to save the folder ID
print(PARENT_FOLDER_ID)

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def get_week_boundaries(date=None):
    if date is None:
        date = datetime.date.today()
    start_of_week = date - datetime.timedelta(days=date.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    return start_of_week, end_of_week

def check_and_create_folder(service, folder_name):
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and '{PARENT_FOLDER_ID}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()

    if results["files"]:
        # If folder exists, delete it
        folder_id = results["files"][0]["id"]
        print(f"Folder {folder_name} exists. Deleting it.")
        service.files().delete(fileId=folder_id).execute()
        print(f"Deleted folder {folder_name}.")
    else:
        print(f"Folder {folder_name} does not exist. Creating a new one.")

    # Create a new folder
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [PARENT_FOLDER_ID]
    }
    new_folder = service.files().create(body=file_metadata, fields='id').execute()
    print(f"Folder '{folder_name}' created. ID: {new_folder.get('id')}")
    return new_folder.get('id')

def save_folder_id(folder_id):
    with open(FOLDER_ID_FILE, 'w') as f:
        f.write(folder_id)

def main():
    if len(sys.argv) != 2:
        print("Usage: python file_name.py <date>")
        return

    input_date = sys.argv[1]
    try:
        date = datetime.datetime.strptime(input_date, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please provide the date in YYYY-MM-DD format.")
        return

    folder_name = f"Files_{input_date}"
    
    # Authenticate and create folder
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    
    # Check if the folder exists, delete if so, and create a new one
    folder_id = check_and_create_folder(service, folder_name)
    
    # Save folder ID to file
    save_folder_id(folder_id)

if __name__ == '__main__':
    main()


# import os
# import datetime
# import sys
# from googleapiclient.discovery import build
# from google.oauth2 import service_account


# SCOPES = ['https://www.googleapis.com/auth/drive']
# SERVICE_ACCOUNT_FILE = "service_account.json"
# PARENT_FOLDER_ID = "1RHpeyvWOBZ-BtjrfQ6rNVTVTC1nBAH1g"  # ID of the parent folder
# FOLDER_ID_FILE = "folder_id.txt"  # File to save the folder ID

# def authenticate():
#     creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#     return creds


# def get_week_boundaries(date=None):
#     if date is None:
#         date = datetime.date.today()
#     # Calculate the starting date of the week containing the provided/specified date (Monday)
#     start_of_week = date - datetime.timedelta(days=date.weekday())
#     # Calculate the ending date of the week containing the provided/specified date (Sunday)
#     end_of_week = start_of_week + datetime.timedelta(days=6)
#     return start_of_week, end_of_week


# def create_folder(service, folder_name):
#     file_metadata = {
#         'name': folder_name,
#         'mimeType': 'application/vnd.google-apps.folder',
#         'parents': [PARENT_FOLDER_ID]
#     }
#     folder = service.files().create(body=file_metadata, fields='id').execute()
#     print('Folder created. ID: ', folder.get('id'))
#     return folder.get('id')

# def save_folder_id(folder_id):
#     with open(FOLDER_ID_FILE, 'w') as f:
#         f.write(folder_id)

# # def main():
# #     current_date = datetime.datetime.now().strftime("%Y-%m-%d")
# #     folder_name = f"Files_{current_date}"
    
# #     # Authenticate and create folder
# #     creds = authenticate()
# #     service = build('drive', 'v3', credentials=creds)
# #     folder_id = create_folder(service, folder_name)
    
# #     # Save folder ID to file
# #     save_folder_id(folder_id)

# def main():
#     if len(sys.argv) != 2:
#         print("Usage: python file_name.py <date>")
#         return

#     input_date = sys.argv[1]
#     try:
#         date = datetime.datetime.strptime(input_date, "%Y-%m-%d").date()
#     except ValueError:
#         print("Invalid date format. Please provide the date in YYYY-MM-DD format.")
#         return

#     folder_name = f"Files_{input_date}"
    
#     # Authenticate and create folder
#     creds = authenticate()
#     service = build('drive', 'v3', credentials=creds)
#     folder_id = create_folder(service, folder_name)
    
#     # Save folder ID to file
#     save_folder_id(folder_id)

# if __name__ == '__main__':
#     main()

