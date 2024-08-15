#!/bin/bash

# Check if the first command line argument exists
if [ -z "$1" ]; then
  echo "Error: First parameter must be the backup file to import."
  exit 1
fi

# If the parameter exists, execute the import.sh script inside the backup container
docker-compose -f docker-compose.develop.yml exec backup ./import.sh "$1"
