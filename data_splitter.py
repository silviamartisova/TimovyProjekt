import numpy as np


def split_to_test_and_train(all_images, all_labels):
    # Split the data into training and testing sets
    split_ratio = 0.8  # 80% for training, 20% for testing
    split_idx = int(len(all_images) * split_ratio)

    train_images = all_images[:split_idx]
    train_labels = all_labels[:split_idx]
    test_images = all_images[split_idx:]
    test_labels = all_labels[split_idx:]

    # Verify the shapes of the resulting sets
    print("Train images shape:", train_images.shape)
    print("Train labels shape:", train_labels.shape)
    print("Test images shape:", test_images.shape)
    print("Test labels shape:", test_labels.shape)

    return train_images, train_labels, test_images, test_labels
