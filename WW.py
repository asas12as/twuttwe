import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import numpy as np

# Load the training data
train_data = tf.keras.utils.image_dataset_from_directory(
    "./dataset/train",
    validation_split=0.2,
    subset="training",
    seed=1337,
    image_size=(180, 180),
    batch_size=32,
)

# Create the model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(180, 180, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dense(10, activation="softmax"))

# Compile the model
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Train the model
model.fit(train_data, epochs=10)

# Evaluate the model
model.evaluate(train_data)

# Save the model
model.save("model.h5")

# Load the test image
test_image = tf.keras.utils.load_img("test.png", target_size=(180, 180))
test_image = np.array(test_image)
test_image = test_image / 255.0

# Predict the class of the test image
prediction = model.predict(test_image)

# Print the class of the test image
print(prediction)
