#!/bin/bash
# import-db.sh

# Parameters
MONGO_HOST="mongodb"  # Name of your MongoDB service in docker-compose
MONGO_PORT="27017"
MONGO_USER=${MONGO_INITDB_ROOT_USERNAME:-root}  # Use environment variable if set, otherwise default to 'root'
MONGO_PASSWORD=${MONGO_INITDB_ROOT_PASSWORD:-example}  # Use environment variable if set, otherwise default to 'example'
BACKUP_NAME=$1  # Pass the backup file name as an argument

if [ -z "$BACKUP_NAME" ]; then
    echo "Error: Backup file name is required."
    exit 1
fi

# Run mongorestore
mongorestore --host $MONGO_HOST --port $MONGO_PORT -u $MONGO_USER -p $MONGO_PASSWORD --authenticationDatabase admin --archive=/$BACKUP_NAME --gzip  --nsExclude 'admin.*'

echo "Database restored from backup: $BACKUP_NAME"
