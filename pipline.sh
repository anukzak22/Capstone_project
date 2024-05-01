#!/bin/bash

# Check if date argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <date>"
    echo "Please specify a date in YYYY-MM-DD format."
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
