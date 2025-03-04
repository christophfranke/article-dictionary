#!/bin/bash

TARGET_DIRECTORY="/root/live"
LOG_FILE="/root/docker-build.log"

# Redirect output to the log file
exec >> "$LOG_FILE" 2>&1

echo "--------------------------------------------------------------------------------"
echo "Build started on: $(date)"

cp .env $TARGET_DIRECTORY

cd $TARGET_DIRECTORY
docker compose down
docker compose build
docker compose up -d

