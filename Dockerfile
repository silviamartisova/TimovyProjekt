# Use the official Python base image
FROM python:3.9

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx

# Set the working directory in the container
WORKDIR /app

# Copy the code into the container
COPY . /app

# Install the required dependencies
RUN pip install tensorflow opencv-python numpy

# Expose port 12345 for the socket server
EXPOSE 12345

# Run the script when the container starts
CMD [ "python", "NNPredictTcpSocket.py" ]
