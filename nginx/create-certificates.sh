#!/bin/sh

# Configuration variables
DOMAINS="www.international-reader.com international-reader.com"
EMAIL="public@krito.de"
WEBROOT_PATH="/var/www/certbot"

# Run Certbot
certbot certonly --webroot -w $WEBROOT_PATH -d $DOMAINS --email $EMAIL --agree-tos --no-eff-email
