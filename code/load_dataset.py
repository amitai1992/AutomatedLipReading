import tensorflow as tf
from keras_preprocessing import image
from keras_preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator()
path = "D:/lip reading final project/lombardgrid/testGen"
train_generator = train_datagen.flow_from_directory(
    directory=path,
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=32,
    class_mode="categorical",
    shuffle=True,
    seed=42
)