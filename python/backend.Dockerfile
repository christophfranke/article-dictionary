# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory to /app/backend
WORKDIR /app/backend

COPY ./backend/requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the current directory contents into the container at /app/backend
COPY ./backend /app/backend

ENV PYTHONPATH="${PYTHONPATH}:/app/shared"
COPY ./shared /app/shared

# Make port 5000 available to the world outside this container
EXPOSE 5000
