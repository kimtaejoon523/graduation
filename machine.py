import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Specify the path to the actual image dataset
train_dir = 'train'  # For example, assume there are folders named 0, 1, 2 in this path

def rgba_to_rgb(img):
    if img.shape[-1] == 4:  # If the number of channels is 4, assume it's RGBA
        return cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img

# Data loading and preprocessing settings
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    preprocessing_function=rgba_to_rgb
)

# Training data generator
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(256, 256),
    batch_size=2,
    class_mode='categorical',
    color_mode='rgb'
)

# Print class indices
class_indices = train_generator.class_indices
print("Class Indices:", class_indices)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu', input_shape=(256, 256, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(train_generator.num_classes, activation='softmax')  # Dynamically assign the number of classes
])

# Compile & train the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
history = model.fit(train_generator, epochs=30)

# Print performance metrics after training
print("Training complete")
print("Model accuracy:", history.history['accuracy'])
print("Model loss:", history.history['loss'])
