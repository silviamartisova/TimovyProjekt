import os
import pyrealsense2 as rs
import cv2
import numpy as np
import socket
import time

# Server address and port
# '0.0.0.0', 12345
# r"D:\School\TimovyProjekt\TimovyProjekt\TestovacieFotky\RealSensePic0.jpg"
server_address = ('0.0.0.0', 12345)

directory = r"C:\Skola_LS_23\Tymovy projekt\TestovacieFotky"
if not os.path.exists(directory):
    os.makedirs(directory)

# Configure RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
color_image = 0

pipeline.start(config)

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
# client_socket.connect(server_address)
# print('Connected to server:', server_address)
photo_path = r"C:\Skola_LS_23\Tymovy projekt\TestovacieFotky\RealSensePic.jpg"

while True:
    time.sleep(8)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(server_address)
    print('Connected to server:', server_address)
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    if not color_frame or not depth_frame:
        raise Exception("Failed to capture frame")

    # Convert RealSense frame to OpenCV format
    color_image = cv2.cvtColor(np.asanyarray(color_frame.get_data()), cv2.COLOR_RGB2BGR)

    filename = os.path.join(directory, "RealSensePic.jpg")
    cv2.imwrite(filename, color_image)

    # Read the photo file as binary data
    with open(photo_path, 'rb') as file:
        photo_data = file.read()

    # Send the photo data to the server
    client_socket.sendall(photo_data)

    # finally:
    # Close the client socket
    client_socket.close()
    client_socket = None

cv2.waitKey(0)
cv2.destroyAllWindows()
pipeline.stop()
client_socket.close()
