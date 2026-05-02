#!/bin/bash

# Check if container is running
if ! docker ps | grep -q primary-db; then
    echo "Error: primary-db container is not running."
    exit 1
fi

echo "Generating CSV data..."
python3 generator.py

echo "Copying files to container..."
docker cp users.csv primary-db:/tmp/users.csv
docker cp posts.csv primary-db:/tmp/posts.csv
docker cp comments.csv primary-db:/tmp/comments.csv

echo "Importing users..."
docker exec primary-db psql -U user -d scaling_test -c "COPY users(id, username, created_at) FROM '/tmp/users.csv' WITH (FORMAT CSV, DELIMITER ',');"

echo "Importing posts..."
docker exec primary-db psql -U user -d scaling_test -c "COPY posts(id, user_id, title, content, created_at) FROM '/tmp/posts.csv' WITH (FORMAT CSV, DELIMITER ',');"

echo "Importing comments..."
docker exec primary-db psql -U user -d scaling_test -c "COPY comments(id, post_id, user_id, comment_text, created_at) FROM '/tmp/comments.csv' WITH (FORMAT CSV, DELIMITER ',');"

echo "Import finished successfully!"
