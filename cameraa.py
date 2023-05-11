import os
import pyrealsense2 as rs
import cv2
import numpy as np

# Configure RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
color_image = 0

pipeline.start(config)

directory = r"C:\Skola_LS_23\Tymovy projekt\TestovacieFotky"
if not os.path.exists(directory):
    os.makedirs(directory)
counter = 0

while True:
    cv2.imshow("fotka", color_image)
    space = cv2.waitKey(1)
    if space == ord(' '):        # Capture a frame from the camera
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame or not depth_frame:
            raise Exception("Failed to capture frame")

        # Convert RealSense frame to OpenCV format
        color_image = cv2.cvtColor(np.asanyarray(color_frame.get_data()), cv2.COLOR_RGB2BGR)
        cv2.imshow("fotka", color_image)
        # Save image
        filename = os.path.join(directory, "RealSensePic{}.jpg".format(counter))
        cv2.imwrite(filename, color_image)
        print("Saved image:", filename)
        counter += 1

cv2.waitKey(0)
cv2.destroyAllWindows()
pipeline.stop()
