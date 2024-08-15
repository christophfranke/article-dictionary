#!/bin/bash

mkdir -p backups/server
rsync -av --ignore-existing root@64.225.101.66:/root/database/backups/ ./backups/server/
