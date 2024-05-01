# Project Setup for Dimensional Pipeline on Stack Overflow Data

## 1. Google API Creation and Setup
1. Go to the Google Cloud Console (https://console.cloud.google.com/).
2. Create a new project and give it a name, like "StackOverflow Data Project".
3. Navigate to the "APIs & Services" section and select "Credentials".
4. Click "Create Credentials" and choose "API key".
5. Save the generated API key to a secure location, preferably in the directory where your Python and SQL files are located. For example:
   - `data_fetching_uploading/service_account.json`

## 2. Google Drive Folder and File ID Setup
1. Create a new Google Drive folder to store your project's files. You can do this in Google Drive or using the Google API.
2. Save the folder ID to a text file for later use. For example:
   - `data_fetching_uploading/folder_id.txt`
3. If you're uploading specific files to Google Drive, create these files and upload them to the folder.
4. Save the file IDs to a separate text file. For example:
   - `data_fetching_uploading/file_id.txt`

## 3. Stack Exchange Account Setup
1. Go to the Stack Exchange website (https://stackexchange.com/).
2. If you don't have an account, create one. You can use it to log in during the data-fetching process.
3. For some operations, you may need authentication with OAuth 2.0 or other Stack Exchange API credentials. Consider creating a Stack Exchange App if needed.
4. If your script requires specific login credentials, ensure that these are stored securely and not exposed in public repositories.

## 4. Alternative Method to Access Google Drive Files
1. You can download the `service_account.json`, `folder_id.txt`, and `file_id.txt` from Google Drive manually by navigating to Credential files.( https://drive.google.com/drive/folders/1cv7UeKxDqznBOiPUs_AiUFERhCKfAhyR?usp=sharing)
2. After downloading, ensure that these files are in the correct directory for the project to access them. This is typically the same directory where the Python and SQL scripts are located, like:
   - `data_fetching_uploading/`

