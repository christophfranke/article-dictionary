# Use an official Python runtime as a parent image (Debian-based)
FROM python:3.12-slim

# Set the working directory to /app/scheduler
WORKDIR /app/scheduler

# Set timezone
RUN apt-get update && apt-get install -y tzdata \
    && ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

# Install SpaCy and build dependencies
RUN apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    cargo \
    bash \
    cmake \
    git \
    python3 \
    python3-dev \
    python3-pip \
    python3-numpy \
    g++

# Upgrade pip, setuptools, and wheel
RUN python3 -m pip install --upgrade pip setuptools wheel

# Install SpaCy
RUN pip3 install spacy

# Install ctranslate2
RUN pip3 install ctranslate2

# Copy and install other Python dependencies
COPY ./scheduler/requirements.txt .
RUN pip3 install -r requirements.txt

# For watch mode in development
RUN pip3 install watchdog

# Setup NLTK
COPY ./setup-nltk.py /app/setup-nltk.py
RUN python3 /app/setup-nltk.py

# Setup Argos
COPY ./setup-argos.py /app/setup-argos.py
RUN python3 /app/setup-argos.py

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app/shared"

# Copy the current directory contents into the container at /app/scheduler
COPY ./scheduler .
COPY ./shared /app/shared

# Command to run the application
CMD ["python3", "main.py"]
