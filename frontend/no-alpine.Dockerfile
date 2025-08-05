# Use an official Node.js runtime as a parent image
FROM node:22-bookworm

# Set the working directory to /app/frontend
WORKDIR /app/frontend

# Copy the package.json and package-lock.json files into the container
COPY ./package*.json .

# Install app dependencies
RUN npm ci

# Copy the rest of the application code into the container
COPY . .

# Cleanup
RUN rm -rf /dist
RUN mkdir -p /dist

RUN npm run build