# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory to /app/backend
WORKDIR /app/scheduler

COPY ./scheduler/requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./setup.py /app/setup.py
RUN python3 /app/setup.py

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app/shared"

# cache buster
RUN date > /app/timestamp.txt

# Copy the current directory contents into the container at /app/backend
COPY ./scheduler .

COPY ./shared /app/shared

# Run app.py when the container launches
CMD ["python3", "main.py"]
