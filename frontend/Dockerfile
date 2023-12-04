# Use an official Node.js runtime as a parent image
FROM node:20

# Set the working directory to /app/dictionary
WORKDIR /app/dictionary

# Copy the package.json and package-lock.json files into the container
COPY ./package*.json .

# Install app dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Build the application
RUN npm run build
