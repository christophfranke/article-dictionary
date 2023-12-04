# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory to /app/backend
WORKDIR /app/backend

# Copy the current directory contents into the container at /app/backend
COPY . /app/backend

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python3", "app.py"]
