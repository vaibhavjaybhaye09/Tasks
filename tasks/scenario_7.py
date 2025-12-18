# “I use Keras preprocessing layers to apply real-time 
# image augmentation like rotation, flipping, and zooming to improve model generalization.”
import tensorflow as tf
from tensorflow.keras import layers

# Image Augmentation Pipeline
data_augmentation = tf.keras.Sequential([
    layers.RandomRotation(0.11),        # ±20 degrees
    layers.RandomFlip("horizontal"),    
    layers.RandomZoom(0.2)               
])

augmented_images = data_augmentation(images)
