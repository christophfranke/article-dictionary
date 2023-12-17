#!/bin/bash
# export-db.sh

# Set the parameters
MONGO_HOST="mongodb"  # Name of your MongoDB service in docker-compose
MONGO_PORT="27017"
MONGO_USER="root"
MONGO_PASSWORD="example"
MONGO_DB="dictionary_app_data"
BACKUP_NAME="/backups/export_$(date +%Y-%m-%d).gz"

# Run mongodump
mongodump --host $MONGO_HOST --port $MONGO_PORT -u $MONGO_USER -p $MONGO_PASSWORD --authenticationDatabase admin --db $MONGO_DB --archive=$BACKUP_NAME --gzip

echo "Backup created: $BACKUP_NAME"
