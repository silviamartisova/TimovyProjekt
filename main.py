import pyrealsense2 as rs
import cv2

# Configure RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start RealSense pipeline
try:
    pipeline.start(config)
except Exception as e:
    print("Camera is not connected. Using notebook webcam instead.")
    cap = cv2.VideoCapture(0)

# Capture a frame from the camera
try:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    if not color_frame or not depth_frame:
        raise Exception("Failed to capture frame")

    # Convert RealSense frame to OpenCV format
    color_image = cv2.cvtColor(np.asanyarray(color_frame.get_data()), cv2.COLOR_BGR2RGB)

    # Save image
    cv2.imwrite("realsense_image.jpg", color_image)

    # Stop RealSense pipeline
    pipeline.stop()
except:
    # Use notebook webcam
    print("Using notebook webcam")
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        # Save image
        cv2.imwrite("webcam_image.jpg", frame)
        cap.release()
    else:
        print("Failed to capture frame from notebook webcam.")