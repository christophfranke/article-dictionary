# Use an official Python runtime as a parent image (Debian-based)
FROM python:3.12.4-slim-bookworm

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

# Install with long compile times
RUN pip3 install spacy
RUN pip3 install ctranslate2

# Setup Argos with long download times
RUN pip3 install argostranslate
COPY ./setup-argos.py /app/setup-argos.py
RUN python3 /app/setup-argos.py

# Setup nltk, will be removed in the future
RUN pip3 install nltk
# Setup NLTK
COPY ./setup-nltk.py /app/setup-nltk.py
RUN python3 /app/setup-nltk.py

RUN python3 -m spacy download en_core_web_lg
RUN python3 -m spacy download el_core_news_lg
RUN python3 -m spacy download de_core_news_lg
RUN python3 -m spacy download es_core_news_lg
RUN python3 -m spacy download ru_core_news_lg
RUN python3 -m spacy download pt_core_news_lg
RUN python3 -m spacy download pl_core_news_lg
RUN python3 -m spacy download it_core_news_lg
RUN python3 -m spacy download fr_core_news_lg

# Copy and install other Python dependencies
COPY ./scheduler/requirements.txt .
RUN pip3 install -r requirements.txt

# For watch mode in development
RUN pip3 install watchdog

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app/shared"

# Copy the current directory contents into the container at /app/scheduler
COPY ./scheduler .
COPY ./shared /app/shared

# Command to run the application
CMD ["python3", "main.py"]
