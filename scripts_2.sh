#!/bin/bash
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

    # Check if a date argument is provided
    if [ $# -eq 1 ]; then
        # Execute the Python script to generate the query with the provided date
        python3 query_creation.py "$1" || continue
    else
        # Execute the Python script to generate the query with the current date
        python3 query_creation.py || continue
    fi

    # Execute the Python script to fetch data for query_comment.sql
    python3 fetching_data.py query_comment.sql || continue
    echo "Second file is saved in downloads"
    sleep 5  # Add a sleep time of 5 seconds

    # Move the downloaded files from Downloads to the current directory
    mv "$HOME/Downloads/QueryResults.csv" . || continue
    echo "Moved QueryResults.csv to the current directory"

    # Activate the virtual environment (if needed)
    # source googledrive/bin/activate || continue

    # python3 data_proc.py || continue
    # echo "file cleaned"
    # Execute the Python script to upload data to Google Drive
    python3 upload_to_folder.py  "$1" 2 || continue
    echo "file saved to the right folder"

    python3 upload_BigQuery.py  "$1" 2 || continue
    echo "file loaded to the BigQuery"

    # Deactivate the virtual environment (if activated)
    # deactivate
    # Remove the downloaded file
    rm QueryResults.csv || continue
    # rm QueryResults_cleaned.csv || continue
    echo "File deleted."


    # If all commands succeed, break out of the loop
    break
done

echo "Script execution completed."
