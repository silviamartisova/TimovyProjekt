import os
import cv2
import numpy as np
import tensorflow as tf
import DataSplitter
from CONSTANTS import image_width, image_height

def load_and_preprocess_images(directory, label):
    images = []
    labels = []

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Adjust file extensions if necessary
            file_path = os.path.join(directory, filename)
            image = cv2.imread(file_path)

            # Convert image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Resize the image
            resized_image = cv2.resize(gray_image, (image_width, image_height))

            # Convert image to numpy array
            image_array = np.array(resized_image, dtype=np.float32)

            # Normalize the image values to range between 0 and 1
            image_array /= 255.0

            # Append the image and label to the lists
            images.append(image_array)
            labels.append(label)

    return images, labels

correct_object_dir = r"C:\Skola_LS_23\Tymovy projekt\Spravne"
incorrect_object_dirs = [r"C:\Skola_LS_23\Tymovy projekt\Nespravne", r"C:\Skola_LS_23\Tymovy projekt\Nespravne2", r"C:\Skola_LS_23\Tymovy projekt\Nespravne3", r"C:\Skola_LS_23\Tymovy projekt\Nespravne4", r"C:\Skola_LS_23\Tymovy projekt\Nespravne5", r"C:\Skola_LS_23\Tymovy projekt\Nespravne6", r"C:\Skola_LS_23\Tymovy projekt\Nespravne7", r"C:\Skola_LS_23\Tymovy projekt\Nespravne8"]




# Load and preprocess correct object images
correct_images, correct_labels = load_and_preprocess_images(correct_object_dir, 1)

# Load and preprocess incorrect object images from multiple directories
incorrect_images = []
incorrect_labels = []

for incorrect_object_dir in incorrect_object_dirs:
    images, labels = load_and_preprocess_images(incorrect_object_dir, 0)
    incorrect_images.extend(images)
    incorrect_labels.extend(labels)

# Combine the correct and incorrect images and labels
all_images = correct_images + incorrect_images
all_labels = correct_labels + incorrect_labels

# Convert the image and label lists to numpy arrays
all_images = np.array(all_images)
all_labels = np.array(all_labels)


# Shuffle the data
indices = np.random.permutation(len(all_images))
all_images = all_images[indices]
all_labels = all_labels[indices]

print("All data loaded!")


############################## NN
num_epochs = 10
batch_size = 32
num_channels = 1
train_images, train_labels, test_images, test_labels = DataSplitter.SplitToTestAndTrain(all_images, all_labels)

def leaky_relu(x):
    return tf.nn.leaky_relu(x)

# Define the neural network architecture
def create_model():
    model = tf.keras.Sequential([
        # Input layer
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(image_width, image_height, num_channels)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        # Hidden layers
        tf.keras.layers.Dense(64, activation='relu'),
        # Output layer
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    return model

# Define the neural network architecture
def create_model2():
    model = tf.keras.Sequential([
        # Input layer
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(image_width, image_height, num_channels)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        # Hidden layers
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation=leaky_relu),
        # Output layer
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    return model


# Create the model
model = create_model2()

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_images, train_labels, epochs=num_epochs, batch_size=batch_size)

# Evaluate the model
loss, accuracy = model.evaluate(test_images, test_labels)
print(f"Test Loss: {loss:.4f}")
print(f"Test Accuracy: {accuracy:.4f}")

# After training the model, save it to a file
model.save('my_model2.h5')
# # Make predictions
# predictions = model.predict(test_images)








