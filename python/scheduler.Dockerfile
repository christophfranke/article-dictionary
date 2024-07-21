# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory to /app/backend
WORKDIR /app/scheduler

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo
RUN python3 -m pip install --upgrade pip setuptools wheel

COPY ./scheduler/requirements.txt .
RUN pip3 install -r requirements.txt

RUN pip3 install watchdog

COPY ./setup.py /app/setup.py
RUN python3 /app/setup.py

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app/shared"

# Copy the current directory contents into the container at /app/backend
COPY ./scheduler .
COPY ./shared /app/shared

CMD ["python3", "main.py"]
