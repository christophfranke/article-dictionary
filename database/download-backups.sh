#!/bin/bash

mkdir -p backups/server
rsync -avzP root@64.225.101.66:/root/database/backups/ ./backups/server/
