#!/bin/bash

# Check if a date argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <date>"
    echo "Please specify a date in YYYY-MM-DD format."
    exit 1
fi

# Validate the date format
if ! [[ $1 =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "Invalid date format. Please provide the date in YYYY-MM-DD format."
    exit 1
fi

# Set the directory where Python scripts are located
SCRIPT_DIR="$(dirname "$0")/data_fetching_uploading"

# Function to reset the execution from the fetch_data.py command
function reset_execution {
    echo "Resetting execution..."
    cd "$SCRIPT_DIR"
}

# Main loop to execute the commands
while true; do
    # Reset execution
    reset_execution

    # Execute the Python script to generate the query with the provided date
    python3 query_creation.py "$1" || continue

    # Execute the Python script to fetch data for query_post.sql
    python3 data_fetching.py query_post.sql || continue
    echo "First file is saved in downloads"
    sleep 5  # Add a sleep time of 5 seconds

    # Move the downloaded files from Downloads to the current directory
    mv "$HOME/Downloads/QueryResults.csv" . || continue
    echo "Moved QueryResults.csv to the current directory"
    # Activate the virtual environment (if needed)
    # source googledrive/bin/activate || continue

    # Execute the Python script to create a Google Drive folder with the provided date
    python3 google_folder_creation.py "$1" || continue
    echo "Created new folder"
    
    # python3 data_proc.py || continue
    # echo "file cleaned"
    # Execute the Python script to upload data to the Google Drive folder
    python3 upload_to_folder.py  "$1" 1 || continue
    echo "file saved to the right folder"

    python3 upload_BigQuery.py  "$1" 1 || continue
    echo "file loaded to the BigQuery"

    # Deactivate the virtual environment (if activated)
    # deactivate
    # Remove the downloaded file
    # rm QueryResults_cleaned.csv || continue
    rm QueryResults.csv || continue
    echo "File deleted."

    # If all commands succeed, break out of the loop
    break

done

echo "First Script execution completed."
