# import os
# import datetime
# from googleapiclient.discovery import build
# from google.oauth2 import service_account

# SCOPES = ['https://www.googleapis.com/auth/drive']
# SERVICE_ACCOUNT_FILE = "service_account.json"

# def authenticate():
#     creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#     return creds

# def get_folder_id():
#     try:
#         with open("folder_id.txt", "r") as f:
#             folder_id = f.read().strip()
#         return folder_id
#     except FileNotFoundError:
#         print("Folder ID file not found.")
#         return None

# def upload_file(file_path):
#     try:
#         creds = authenticate()
#         service = build('drive', 'v3', credentials=creds)
#         current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         current_date = datetime.datetime.now().strftime("%Y%m%d")
#         filename = f"query_results_{current_date}.csv"
#         folder_id = get_folder_id()
#         if folder_id:
#             file_metadata = {
#                 'name': filename,
#                 'parents': [folder_id]
#             }
#             media_body = os.path.abspath(file_path)  # Ensure absolute path
#             file = service.files().create(body=file_metadata, media_body=media_body).execute()
#             print("File uploaded successfully.")
#             return True 
#         else:
#             print("Folder ID not available.")
#             return False
#     except Exception as e:
#         print(f"An error occurred while uploading the file: {e}")
#         return False

# file_id=upload_file("QueryResults.csv")
# # upload_file("QueryResults-2.csv")


# import os
# import datetime
# from googleapiclient.discovery import build
# from google.oauth2 import service_account

# SCOPES = ['https://www.googleapis.com/auth/drive']
# SERVICE_ACCOUNT_FILE = "service_account.json"

# def authenticate():
#     creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#     return creds

# def get_folder_id():
#     try:
#         with open("folder_id.txt", "r") as f:
#             folder_id = f.read().strip()
#         return folder_id
#     except FileNotFoundError:
#         print("Folder ID file not found.")
#         return None

# def save_file_id(file_id):
#     try:
#         with open("file_id.txt", "a") as f:
#             current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             f.write(f"{current_datetime}: {file_id}\n")
#             print("File ID saved to file_id.txt.")
#     except Exception as e:
#         print(f"An error occurred while saving the file ID: {e}")



# def get_week_boundaries(date=None):
#     if date is None:
#         date = datetime.date.today()
#     # Calculate the starting date of the week containing the provided/specified date (Monday)
#     start_of_week = date - datetime.timedelta(days=date.weekday())
#     # Calculate the ending date of the week containing the provided/specified date (Sunday)
#     end_of_week = start_of_week + datetime.timedelta(days=6)
#     return start_of_week, end_of_week


# def upload_file(file_path):
#     try:
#         creds = authenticate()
#         service = build('drive', 'v3', credentials=creds)
#         current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         current_date = datetime.datetime.now().strftime("%Y%m%d")
#         filename = f"query_results_{current_date}.csv"
#         folder_id = get_folder_id()
#         if folder_id:
#             file_metadata = {
#                 'name': filename,
#                 'parents': [folder_id]
#             }
#             media_body = os.path.abspath(file_path)  # Ensure absolute path
#             file = service.files().create(body=file_metadata, media_body=media_body).execute()
#             print("File uploaded successfully.")
#             file_id = file.get('id')  # Get the file ID
#             save_file_id(file_id)  # Save the file ID to file_id.txt
#             return file_id 
#         else:
#             print("Folder ID not available.")
#             return False
#     except Exception as e:
#         print(f"An error occurred while uploading the file: {e}")
#         return False

# file_id = upload_file("QueryResults.csv")
# # upload_file("QueryResults-2.csv")
import os
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
import sys

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "service_account.json"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def get_folder_id():
    try:
        with open("folder_id.txt", "r") as f:
            folder_id = f.read().strip()
        return folder_id
    except FileNotFoundError:
        print("Folder ID file not found.")
        return None

def save_file_id(file_id):
    try:
        with open("file_id.txt", "a") as f:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{current_datetime}: {file_id}\n")
            print("File ID saved to file_id.txt.")
    except Exception as e:
        print(f"An error occurred while saving the file ID: {e}")

def get_week_boundaries(date):
    # Calculate the starting date of the week containing the provided date (Monday)
    start_of_week = date - datetime.timedelta(days=date.weekday())
    # Calculate the ending date of the week containing the provided date (Sunday)
    end_of_week = start_of_week + datetime.timedelta(days=6)
    return start_of_week, end_of_week

def upload_file(file_path, date, number):
    try:
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)
        
        # Parse the date argument
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        
        week_start, week_end = get_week_boundaries(date_obj)
        week_start_str = week_start.strftime("%Y-%m-%d")
        week_end_str = week_end.strftime("%Y-%m-%d")
        
        filename = f"query_results_{week_start_str}_{week_end_str}_{number}.csv"
        
        folder_id = get_folder_id()
        if folder_id:
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            media_body = os.path.abspath(file_path)  # Ensure absolute path
            file = service.files().create(body=file_metadata, media_body=media_body).execute()
            print("File uploaded successfully.")
            file_id = file.get('id')  # Get the file ID
            save_file_id(file_id)  # Save the file ID to file_id.txt
            return file_id 
        else:
            print("Folder ID not available.")
            return False
    except Exception as e:
        print(f"An error occurred while uploading the file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 upload_to_folder.py <date> <number>")
        sys.exit(1)

    file_path = "QueryResults.csv"
    # file_path = "QueryResults_cleaned.csv" # Update with your file path
    date = sys.argv[1]
    number = sys.argv[2]
    upload_file(file_path, date, number)
