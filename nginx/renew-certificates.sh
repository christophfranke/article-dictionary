#!/bin/sh

# Configuration variables
DOMAIN="articles.krito.de"
EMAIL="public@krito.de"
WEBROOT_PATH="/var/www/certbot"

# Renewing the certificate
certbot renew --webroot -w $WEBROOT_PATH -d $DOMAIN --email $EMAIL --agree-tos --no-eff-email

# Reload Nginx to apply the renewed certificate (optional, uncomment if needed)
nginx -s reload
