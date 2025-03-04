#!/bin/bash

target_directory="/root/live"
log_file="/root/docker-build.log"

# Redirect output to the log file
exec >> "$log_file" 2>&1

echo "--------------------------------------------------------------------------------"
echo "Build started on: $(date)"

cp .env $target_directory

cd $target_directory
docker compose down
docker compose build
docker compose up -d

