#!/bin/sh

# Configuration variables
DOMAIN="www.international-reader.com"
EMAIL="public@krito.de"
WEBROOT_PATH="/var/www/certbot"

# Run Certbot
certbot certonly --webroot -w $WEBROOT_PATH -d $DOMAIN --email $EMAIL --agree-tos --no-eff-email

