import os
import pyrealsense2 as rs
import cv2
import numpy as np

# Configure RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
color_image = 0

# Create folder to save images if it doesn't exist
directory = r"C:\Users\sisim\Desktop\FEI\1. rok ING\LS\TP\RealSensePhoto\ImagesUNS"
if not os.path.exists(directory):
    os.makedirs(directory)

# Start RealSense pipeline
try:
    pipeline.start(config)
except Exception as e:
    print("Camera is not connected. Using notebook webcam instead.")
    cap = cv2.VideoCapture(0)

# Initialize image counter
count = 1

# Loop to capture images
while True:
    # Wait for key press
    key = cv2.waitKey(1)
    if key == ord(' '):
        try:
            # Capture a frame from the camera
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not color_frame or not depth_frame:
                raise Exception("Failed to capture frame")

            # Convert RealSense frame to OpenCV format
            color_image = cv2.cvtColor(np.asanyarray(color_frame.get_data()), cv2.COLOR_BGR2RGB)

            # Save image
            filename = os.path.join(directory, "RealSensePic{}.jpg".format(count))
            cv2.imwrite(filename, color_image)
            print("Saved image:", filename)

            # Increment image counter
            count += 1

        except:
            # Use notebook webcam
            print("Using notebook webcam")
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                # Save image
                filename = os.path.join(directory, "WebcamPic{}.jpg".format(count))
                cv2.imwrite(filename, frame)
                print("Saved image:", filename)
                cap.release()
                # Increment image counter
                count += 1
            else:
                print("Failed to capture frame from notebook webcam.")

    elif key == ord('0'):
        break

    # Update the frame display and listen to keyboard events
    cv2.imshow("RealSense Capture", color_image)
    cv2.waitKey(1)

# Stop RealSense pipeline
pipeline.stop()