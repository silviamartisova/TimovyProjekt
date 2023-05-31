import tensorflow as tf
import cv2
import numpy as np

# Load the saved model from the file
model = tf.keras.models.load_model('../my_model.h5')
# model = tf.keras.models.load_model('my_model2.h5')

image_width = 64
image_height = 64


# Preprocess a single photo
def preprocess_photo(_photo_path):
    # Load the photo
    photo = cv2.imread(_photo_path)
    cv2.imshow("vzorka", photo)

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


# Path to the photo you want to evaluate
# photo_path = r"C:\Skola_LS_23\Tymovy projekt\Nespravne\RealSensePic89.jpg"
# photo_path = r"C:\Skola_LS_23\Tymovy projekt\Spravne\RealSensePic689.jpg"
# photo_path = r"C:\Skola_LS_23\Tymovy projekt\Nespravne8\RealSensePic136.jpg"
photo_path = r"C:\Skola_LS_23\Tymovy projekt\TestovacieFotky\RealSensePic0.jpg"

# Preprocess the photo
preprocessed_photo = preprocess_photo(photo_path)

# Use the loaded model for prediction
prediction = model.predict(preprocessed_photo)

# The prediction will be a probability value, you can interpret it accordingly
print("Prediction:", prediction)

# Set the threshold value
threshold = 0.5

# Convert the prediction to 0 or 1 based on the threshold
prediction_binary = 1 if prediction[0][0] >= threshold else 0

# Print the binary prediction
print("Binary Prediction:", prediction_binary)

cv2.waitKey(0)
cv2.destroyAllWindows()
