# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory to /app/backend
WORKDIR /app/scheduler

COPY ./scheduler/requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the current directory contents into the container at /app/backend
COPY ./scheduler .

# Set PYTHONPATH to include the shared directory
ENV PYTHONPATH="${PYTHONPATH}:/shared"
COPY ./shared /shared

# Run app.py when the container launches
CMD ["python3", "main.py"]
