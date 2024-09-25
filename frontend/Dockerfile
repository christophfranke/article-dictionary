# Use an official Node.js runtime as a parent image
FROM node:22-alpine3.20

# Set the working directory to /app/frontend
WORKDIR /app/frontend

# Copy the package.json and package-lock.json files into the container
COPY ./package*.json .

# Install app dependencies
RUN npm ci

RUN rm -rf /dist
RUN mkdir -p /dist

# Copy the rest of the application code into the container
COPY . .

RUN npm run build