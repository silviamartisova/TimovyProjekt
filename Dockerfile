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
RUN apt update \
    && apt install -y software-properties-common python3-pip \
    && add-apt-repository ppa:gijzelaar/snap7 \
    && apt update \
    && apt install -y libsnap7-dev libsnap7-1 \

RUN apt install python-snap7  - ????
RUN pip3 install .


# Expose port 12345 for the socket server
EXPOSE 12345

# Run the script when the container starts
CMD [ "python", "NNPredictTcpSocket.py" ]
