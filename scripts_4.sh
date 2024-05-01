SCRIPT_DIR="$(dirname "$0")/data_fetching_uploading"

cd "$SCRIPT_DIR"
if [ -z "$1" ]; then
  echo "Usage: $0 <date (YYYY-MM-DD)>"
  exit 1
fi

python3 creating_view_post.py  "$1"
python3 creating_view_comments.py  "$1"
python3 bigquery_to_drive.py "view_posts_$1.csv"
python3 bigquery_to_drive.py "view_comments_$1.csv"

# Files to delete
FILES_TO_DELETE=("view_posts_$1.csv" "view_comments_$1.csv")

# Loop through the list of files to delete them
for FILE in "${FILES_TO_DELETE[@]}"; do
    if [ -f "$FILE" ]; then
        rm "$FILE"
        echo "Deleted file: $FILE"
    else
        echo "File not found: $FILE"
    fi
done

echo "Bash script completed."
