SCRIPT_DIR="$(dirname "$0")/data_fetching_uploading"

cd "$SCRIPT_DIR"
# Execute the Python script
python3 table_creation.py
