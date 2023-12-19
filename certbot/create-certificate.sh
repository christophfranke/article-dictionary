#!/bin/bash

# Configuration variables
DOMAIN="articles.krito.de"
EMAIL="public@krito.de"
WEBROOT_PATH="/var/www/certbot"

# Run Certbot
docker-compose run --rm certbot certonly --webroot -w $WEBROOT_PATH -d $DOMAIN --email $EMAIL --agree-tos --no-eff-email

