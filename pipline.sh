#!/bin/bash

# Check if date argument is provided
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

# Check if the date is valid using Python
python3 -c "
from datetime import datetime
import sys
try:
    datetime.strptime(sys.argv[1], '%Y-%m-%d')
except ValueError:
    sys.exit(1)
" "$1"

if [ $? -ne 0 ]; then
    echo "Invalid date. The provided date does not seem to be a real date."
    exit 1
fi
# Run first bash script with the provided date argument
echo "Running first script with date argument: $1"
./scripts_1.sh "$1"

# Wait for 5 minutes
echo "Waiting for 5 minutes..."
sleep 50 

# Run second bash script
echo "Running second script..."
./scripts_2.sh "$1"

echo "Running third script..."
./scripts_3.sh "$1"

echo "Running forth script..."
./scripts_4.sh "$1"

echo "All scripts have been executed."
