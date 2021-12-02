import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
import argparse

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

#Input parameters
MODEL_DIR = os.path.abspath(os.environ.get('MODEL_DIR', os.getcwd() + '/models'))

#Download Fashion MNIST dataset and split it for train and test
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

#Scale images
train_images = train_images / 255.0
test_images = test_images / 255.0

#Reshape array
train_images = train_images.reshape(train_images.shape[0], 28, 28, 1)
test_images = test_images.reshape(test_images.shape[0], 28, 28, 1)

#Build Keras model
model = keras.Sequential([
  keras.layers.Conv2D(input_shape=(28,28,1), filters=8, kernel_size=3, 
                      strides=2, activation='relu', name='Conv1'),
  keras.layers.Flatten(),
  keras.layers.Dense(10, activation=tf.nn.softmax, name='Softmax')
])

model.summary()

#Read the EPOCH value from environment variable
epochs = int(os.getenv("EPOCHS",1))

#Compile and fit
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=epochs)

#Check accuracy
test_loss, test_acc = model.evaluate(test_images, test_labels)
print('\nModel accuracy: {}'.format(test_acc))

#Save model 
export_path = os.path.join(MODEL_DIR)
print('export_path = {}\n'.format(export_path))

model.save(MODEL_DIR)

print('\nModel saved to ' + MODEL_DIR)
