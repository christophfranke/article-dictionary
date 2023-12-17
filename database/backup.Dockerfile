# Use the same MongoDB image
FROM mongo:latest

# Create a directory for scripts
RUN mkdir -p /scripts

# Set working directory and add it to path
WORKDIR /scripts
ENV PATH="/scripts:${PATH}"

# Copy both the backup and restore scripts
COPY ./scripts .

# Set permissions for the scripts
RUN chmod +x /scripts/*.sh

# Keep the container running (since we'll be using docker exec to run scripts)
CMD ["tail", "-f", "/dev/null"]
