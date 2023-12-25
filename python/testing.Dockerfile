# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory to /app/backend
WORKDIR /app

COPY ./testing/requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./setup.py /app/setup.py
RUN python3 /app/setup.py

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app/shared:/app/backend"

# cache buster
RUN date > /app/timestamp.txt

COPY ./shared /app/shared
COPY ./backend /app/backend
COPY ./testing /app/testing
