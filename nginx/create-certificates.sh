#!/bin/sh

# Configuration variables
DOMAIN="international-reader.com"
SUBDOMAINS="www.international-reader.com"
EMAIL="public@christophfranke.info"
WEBROOT_PATH="/var/www/certbot"

# Prepare the -d options for Certbot
DOMAINS_OPTION="-d $DOMAIN"
for SUBDOMAIN in $SUBDOMAINS; do
    DOMAINS_OPTION="$DOMAINS_OPTION -d $SUBDOMAIN"
done

# Run Certbot
certbot certonly --webroot -w $WEBROOT_PATH $DOMAINS_OPTION --email $EMAIL --agree-tos --no-eff-email
