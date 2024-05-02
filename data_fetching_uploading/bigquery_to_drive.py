import os
import datetime
import sys
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
# Define the Google Drive API scope and service account file path
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "service_account.json"
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Function to get the Google Drive folder ID from a file
config_path= "config.json"
with open(config_path, 'r') as file:
    config = json.load(file)
folder_id = config.get("view_folder_id", None)

# Function to save the file ID with a timestamp to a text file
# def save_file_id(file_id):
#     try:
#         with open("view_id.txt", "a") as f:
#             current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             f.write(f"{current_datetime}: {file_id}\n")
#             print("File ID saved to view_id.txt.")
#     except Exception as e:
#         print(f"An error occurred while saving the file ID: {e}")

# Function to upload a file to Google Drive, replacing existing file if it has the same name
# def upload_file(file_path, creds,folder_id):
#     try:
#         service = build('drive', 'v3', credentials=creds)
#         if folder_id:
#             # Check if a file with the same name exists in the folder
#             filename = os.path.basename(file_path)
#             query = f"name='{filename}' and '{folder_id}' in parents"
#             existing_files = service.files().list(q=query, fields="files(id)").execute().get("files", [])

#             # If an existing file is found, delete it
#             if existing_files:
#                 for file in existing_files:
#                     file_id = file["id"]
#                     service.files().delete(fileId=file_id).execute()
#                 print(f"Deleted existing file(s) with name '{filename}'.")
#             else:
#                 print("no file found")

#             # Create file metadata and upload the new file
#             file_metadata = {
#                 'name': filename,
#                 'parents': [folder_id]
#             }
#             media_body = os.path.abspath(file_path)
#             new_file = service.files().create(body=file_metadata, media_body=media_body).execute()
#             print("File uploaded successfully.")
#             new_file_id = new_file.get('id')
#             # save_file_id(new_file_id)  # Save the new file ID

#             return new_file_id
#         else:
#             print("Folder ID not available.")
#             return False
#     except Exception as e:
#         print(f"An error occurred while uploading the file: {e}")
#         return False

# # Main script execution
# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python3 upload_to_folder.py <file_path>")
#         sys.exit(1)

#     # Get the file path from the command-line argument
#     file_path = sys.argv[1]

#     # Upload the file to Google Drive, replacing existing files with the same name
#     upload_file(file_path, creds,folder_id)

def upload_file_with_retry(file_path, creds, folder_id, retries=3, delay=10):
    try:
        # Create Google Drive service
        service = build('drive', 'v3', credentials=creds)
        while retries > 0:
            try:
                if folder_id:
                    filename = os.path.basename(file_path)
                    
                    # Check for existing files with the same name
                    query = f"name='{filename}' and '{folder_id}' in parents"
                    existing_files = service.files().list(q=query, fields="files(id)").execute().get("files", [])

                    # Delete existing files with the same name
                    if existing_files:
                        for file in existing_files:
                            file_id = file["id"]
                            service.files().delete(fileId=file_id).execute()
                        print(f"Deleted existing file(s) with name '{filename}'.")
                    
                    # Create the file metadata and upload the new file
                    file_metadata = {'name': filename, 'parents': [folder_id]}
                    with open(file_path, 'rb') as media_file:
                        media = MediaFileUpload(media_file.name, resumable=True)
                        new_file = service.files().create(body=file_metadata, media_body=media).execute()
                    
                    print("File uploaded successfully.")
                    return new_file.get('id')  # Return the ID of the newly uploaded file
                else:
                    print("Folder ID not available.")
                    return False
                
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:  # Server errors
                    retries -= 1
                    time.sleep(delay)
                else:
                    raise  # Re-raise for non-retryable errors
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return False
    except Exception as e:
        print(f"An error occurred while setting up the Google Drive service: {e}")
        return False

# Main script execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 bigquery_to_drive.py <file_path>")
        sys.exit(1)

    # Get the file path from the command-line argument
    file_path = sys.argv[1]

    # Upload the file to Google Drive, with retry logic
    upload_file_with_retry(file_path, creds, folder_id)