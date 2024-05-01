#!/bin/bash

# Determine the script's current directory
SCRIPT_DIR="$(dirname "$0")/data_fetching_uploading"

cd "$SCRIPT_DIR"
# Path to the virtual environment (relative to script directory)
# source googledrive/bin/activate || continue


# Check if a date argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <date (YYYY-MM-DD)>"
  exit 1
fi

# Run the Python script with the given date argument
python insert_to_staging.py "$1"

# Run the Python script with the given date argument and a 2-second delay between executions

python updating_dim_users.py "$1" 
echo "Updated Dim_Users table"


python updating_fact_posts.py "$1"
echo "Updated Fact_Posts table"


python updating_fact_comments.py "$1"
echo "Updated Fact_Comments table"

python updating_bridge_posts_tags.py "$1"
echo "Updated Bridge_Posts_Tags table"


python updating_dim_tags.py "$1"
echo "Updated Dim_Tags table"

python updating_bridge_posts_comments.py "$1"
echo "Updated Bridge_Posts_Comments table"

python updating_dim_date.py "$1"
echo "Updated Dim_Date table"