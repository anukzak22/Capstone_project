# Project Setup for Dimensional Pipeline on Stack Overflow Data and Execution

This guide outlines the steps to set up and run the pipeline. Follow these instructions to ensure proper configuration and execution.

## Prerequisites
- Google Drive account
- Google Cloud Platform (GCP) account
- Stack overflow acount
- Selenium installed and configured
- A Safari web browser for Selenium
- Reuqirments.txt packages 

## Step 1: Set Up Google Drive Folders
1. **Create a Parent Folder**:
   - Create a new folder in Google Drive to store the raw and view tables.

2. **Create Subfolders**:
   - Inside the parent folder, create two subfolders:
     - `raw_table`
     - `view_table`

3. **Retrieve Folder IDs**:
   - Right-click on each folder and select "Get link."
   - Note the folder IDs for `raw_table` and `view_table`.

## Step 2: Create the Configuration File
Create a JSON configuration file with the following information and save it into the `data_fetching_uploading` folder:
- **Google Drive Information**:
  - Raw_table ID for `raw_table`: `"raw_table_id": "YOUR_PARENT_FOLDER_ID"`
  - Folder ID for `view_table`: `"view_folder_id": "YOUR_VIEW_FOLDER_ID"`

- **BigQuery Dataset Information**:
  - Dataset ID for your BigQuery: `"dataset_id": "YOUR_DATASET_ID"`
  (this is the name you want the database to have)

- **Stack Overflow Credentials**:
  - Stack Overflow email: `"email": "YOUR_EMAIL"`
  - Stack Overflow password: `"password": "YOUR_PASSWORD"`

- **Google Cloud Platform (GCP) Information**:
  - Project ID for your GCP project
  - Path to your `service_account.json` file

```json
{
    "view_folder_id": "view_tables_folder_id",
    "dataset_id": "datbase_name",
    "email": "YOUR_EMAIL",
    "password": "YOUR_PASSWORD",
    "raw_table_id": "raw-data_folder-id"
}

``` 
## Step 3: Set Up Google Cloud Platform

To use Google Cloud Platform (GCP) services like BigQuery and Google Drive programmatically, you need to create a GCP project and set up a service account with appropriate permissions. Follow these steps:

### 3.1 Create a GCP Project
1. Visit the GCP Console: [Google Cloud Console](https://console.cloud.google.com/).
2. Click on "Select a Project" at the top of the page, then click "New Project."
3. Provide a name for your project and click "Create."
4. After creating the project, note the project ID. You will need this information later.

### 3.2 Create a Service Account
1. In the GCP Console, go to "IAM & Admin" > "Service Accounts."
2. Click "Create Service Account."
3. Give your service account a name and description.
4. Click "Create and Continue."
5. Assign the "Owner" role to yourself to ensure you have full permissions.
6. Click "Done."
7. Find the service account you just created and click the three-dot menu in the "Actions" column.
8. Select "Manage Keys."
9. Click "Add Key," then choose "Create New Key."
10. Select the "JSON" format for the key.
11. Download the key and save it as `service_account.json`.

### 3.3 Save Service Account and Config File
1. After downloading the `service_account.json`, save it in the appropriate folder (usually the `data-fetching-uploading` folder).
2. Ensure the configuration file (as described in Step 2) is in the same folder.v

### 3.4 Share Google Drive Folder with the Service Account
1. Open Google Drive.
2. Right-click on your parent folder (from Step 1) and choose "Share."
3. Paste the email from the service account JSON key.
4. Grant "Editor" access to the folder.
5. Click "Send."

### 3.5 Assign Permissions in BigQuery
1. Open the GCP Console and go to "BigQuery."
2. Select your project from the dropdown.
3. In the "IAM & Admin" section, go to "IAM."
4. Click "Grant Access."
5. Add the service account email and assign the following roles:
   - "BigQuery Admin"
   - "BigQuery Job User"
6. Click "Save."

## Step 4: Run the Pipeline
With everything set up, you can now run the pipeline.

### 4.1 Ensure Configuration Files Are in Place
1. Make sure you have a configuration file with the correct details (as outlined in Step 2).
2. Ensure that `service_account.json` and the `config.json` are in the correct location `data_fetching_uploading` folder .

### 4.2 Execute the Pipeline
1. Use your preferred method (such as a Python script, terminal, or Colab notebook) to run the pipeline.
2. Ensure that the pipeline executes without errors and completes all the steps.

### 4.3 Perform Final Checks
1. Confirm that data has been downloaded and saved to Google Drive.
2. Verify that the BigQuery tables have been created and populated correctly.
3. Check any logging or output for errors or issues.

## Troubleshooting
If you encounter any issues, consider the following:
- **Configuration Errors**:
  - Ensure all configuration values are correct, including folder IDs, dataset IDs, and credentials.
- **Permission Errors**:
  - Confirm that the service account has appropriate permissions and access to Google Drive and BigQuery.
- **Missing Dependencies**:
  - Check that all necessary software, libraries, and dependencies are installed and configured correctly.
- **Review Error Messages**:
  - Examine any error messages for clues about the source of the problem.


### Alternative: Use Pre-configured Credentials
If the above steps do not resolve the issue, you can use pre-configured credentials:
1. Go to the following link on Google Drive: [Download Credentials Link](#).
2. Download the `config_json` file and `service_account.json`.
3. Add these files to the correct directory (usually the `data_fetching_uploading` folder).
4. Re-run the pipeline with these credentials.

## Step 5: Run the Pipeline

To run the pipeline, you need to execute a series of bash scripts in a specific sequence. It's recommended to run `script_0.sh` first, followed by `pipeline.sh`. Below is the step-by-step process for running the pipeline.

### 5.1 Run `script_0.sh`
1. Open a terminal and navigate (`cd`) to the directory where the bash scripts are located.
2. Run the `script_0.sh` script to initialize the database and create the necessary dimensional and fact tables based on the `config.json` file's `dataset_id`:
   ```bash
   ./script_0.sh
   ```
### 5.2 Run `pipeline.sh`
After initializing the database with `script_0.sh`, you can run the main pipeline script, `pipeline.sh`, to fetch the week's data and perform the rest of the pipeline operations. This script takes a date argument representing a Sunday date to fetch the data for the corresponding week.

1. Ensure you are in the correct directory where the bash files are located.
2. Run `pipeline.sh` with a specific Sunday date as an argument(to contain whole weeks data):
   ```bash
   ./pipeline.sh <date argument>
   ```
   Example 
   ```bash
   ./pipeline.sh 2024-04-07
   ```
This command fetches data from the week starting from 2024-04-01 to 2024-04-07 and carries out the pipeline's subsequent operations. The pipeline performs various tasks including:

- **Fetching Data**:
  - Downloads data using Selenium based on the date range provided by the `pipeline.sh` argument.
- **Uploadingm to Drive**:
  - The downloaded data is uploaded in Google Drive within the appropriate subfolder (`raw_table`).
- **Uploading to BigQuery**:
  - The Drive data is uploaded to BigQuery, with separate temporary tables being merged into a staging_raw_table.
- **Updating BigQuery Tables**:
  - The pipeline updates the dimensional and fact tables in BigQuery with the new data from staging_raw_table.
- **Creating View Tables**:
  - Creates 2 view tables in BigQuery one for **comment** another one for **posts** for further analysis.

After running `pipeline.sh`, you can check for successful pipeline execution by examining the following:

- **Google Drive**:
  - Ensure the correct files have been saved in the `raw_table` and `view_table` folders.
- **BigQuery**:
  - Confirm that the new data has been uploaded to BigQuery and that the staging table and other tables have been updated.
- **Terminal Output**:
  - Review the output for any errors or warning messages that could indicate issues during execution.If the terminal outputs messages about successful outputs and then finishes without errors. Then the process is completed without errors

### Troubleshooting Tips
If any problems occur during or after running `pipeline.sh`:

- **Check the Pipeline Argument**:
  - Make sure you specified a valid Sunday date.
- **Ensure Successful Initialization**:
  - Confirm that `script_0.sh` was run and completed without errors before running `pipeline.sh`.
- **Examine Configuration Files**:
  - Check the `config_json` and `service_account.json` files for correctness and completeness.
- **Look for Errors**:
  - If the pipeline fails, inspect the error messages to identify the cause. Common issues include incorrect folder IDs,directory issues or permission problem.
