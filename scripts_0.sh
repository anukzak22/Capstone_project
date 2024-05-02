SCRIPT_DIR="$(dirname "$0")/data_fetching_uploading"

cd "$SCRIPT_DIR"
# Execute the Python script

python3 creating_dataset.py
python3 creating_dbtables.py
