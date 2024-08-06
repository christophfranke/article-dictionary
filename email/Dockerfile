# Use the official Alpine Linux image as a base
FROM alpine:3.20.2

# Install necessary packages
RUN apk update && apk add --no-cache \
    postfix \
    postfix-pcre \
    postfix-ldap \
    postfix-mysql \
    postfix-pgsql \
    opendkim \
    rsyslog \
    openssl

# Create directories for DKIM keys and Postfix configuration
RUN mkdir -p /etc/opendkim/keys /etc/postfix

# Generate DKIM keys
RUN openssl genrsa -out /etc/opendkim/keys/dkim.private 2048 && \
    openssl rsa -in /etc/opendkim/keys/dkim.private -pubout -out /etc/opendkim/keys/dkim.public

# Copy the configuration files into the container
COPY opendkim/opendkim.conf /etc
COPY opendkim/KeyTable /etc/opendkim/
COPY opendkim/SigningTable /etc/opendkim/
COPY postfix/main.cf /etc/postfix/
COPY rsyslog.conf /etc/rsyslog.conf

# Set appropriate permissions
RUN chown -R root:root /etc/opendkim && \
    chmod 700 /etc/opendkim && \
    chmod 400 /etc/opendkim/keys/dkim.private

# Expose ports for Postfix
EXPOSE 25

# Start Rsyslog, OpenDKIM, and Postfix
# Using `sh` to run multiple commands in a single `CMD`
CMD sh -c "rsyslogd && \
    opendkim -x /etc/opendkim.conf && \
    postfix start-fg"
