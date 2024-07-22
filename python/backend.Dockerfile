# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory to /app/backend
WORKDIR /app/backend

COPY ./backend/requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./setup-nltk.py /app/setup-nltk.py
RUN python3 /app/setup-nltk.py

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app/shared"

COPY ./shared /app/shared

# Copy the current directory contents into the container at /app/backend
COPY ./backend /app/backend
