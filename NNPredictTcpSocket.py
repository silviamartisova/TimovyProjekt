import tensorflow as tf
import cv2
import numpy as np
import socket
from datetime import datetime

image_width = 64
image_height = 64

# Load the saved model from the file
model = tf.keras.models.load_model('my_model.h5')


# Preprocess a single photo
def preprocess_photo(photo):
    # Convert the photo to grayscale
    gray_photo = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)

    # Resize the photo to the desired input shape
    resized_photo = cv2.resize(gray_photo, (image_width, image_height))

    # Convert the photo to a numpy array
    photo_array = np.array(resized_photo, dtype=np.float32)

    # Normalize the photo values to the range [0, 1]
    photo_array /= 255.0

    # Add a batch dimension to the photo array
    photo_array = np.expand_dims(photo_array, axis=0)

    return photo_array


# Set up TCP socket server
def run_socket_server():
    # Create a TCP socket
    # The prediction will be a probability value, you can interpret it accordingly
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"[{current_time}] Socket server is running and waiting for a connection...")
    try:
        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Accepted connection from:", client_address)

            try:
                # Receive the photo from the client
                photo_data = b''
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    photo_data += data

                # Convert the received data to a numpy array
                nparr = np.frombuffer(photo_data, np.uint8)

                # Decode the numpy array into an OpenCV image
                photo = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Preprocess the photo
                preprocessed_photo = preprocess_photo(photo)

                # Use the loaded model for prediction
                prediction = model.predict(preprocessed_photo)

                # The prediction will be a probability value, you can interpret it accordingly
                print("Prediction:", prediction)
                # Set the threshold value
                threshold = 0.5

                # Convert the prediction to 0 or 1 based on the threshold
                prediction_binary = 1 if prediction[0][0] >= threshold else 0

                # Print the binary prediction
                # The prediction will be a probability value, you can interpret it accordingly
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{current_time}] Binary Prediction:", prediction_binary)

            except Exception as e:
                print(f"[{current_time}] Error occurred:", str(e))

            finally:
                # Close the client socket
                client_socket.close()
    except KeyboardInterrupt:
        print('Server stopped by keyboard interrupt')
        server_socket.close()


# Run the socket server
run_socket_server()