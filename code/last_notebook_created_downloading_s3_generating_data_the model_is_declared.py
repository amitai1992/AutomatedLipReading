#!/usr/bin/env python
# coding: utf-8

# In[11]:


from sagemaker import get_execution_role 


role = get_execution_role() 

bucket = 'alr-data' 
data_key = 'validation' 
data_location = 's3://{}/{}'.format(bucket, data_key)


# In[12]:


import boto3
import os
s3 = boto3.resource('s3') # assumes credentials & configuration are handled outside python in .aws directory or environment variables

def download_s3_folder(bucket_name, s3_folder, local_dir=None):
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: a relative or absolute directory path in the local file system
    """
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix = s3_folder):
        target = obj.key if local_dir is None             else os.path.join(local_dir, os.path.basename(obj.key))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        try:
            bucket.download_file(obj.key, target)
        except:
            continue


# In[13]:


download_s3_folder(bucket,data_key)


# In[19]:


from keras_preprocessing import image
from keras_preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator()
path_for_trainset = "train"
path_for_testset = "test"
path_for_validationset = "validation"

print("train set:")
train_generator = datagen.flow_from_directory(
    directory=path_for_trainset,
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=32,
    class_mode="categorical",
    shuffle=True,
    seed=42
)

print("validation set:")
validation_generator = datagen.flow_from_directory(
    directory=path_for_validationset,
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=32,
    class_mode="categorical",
    shuffle=True,
    seed=42
)

print("test set:")
test_generator = datagen.flow_from_directory(
    directory=path_for_testset,
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=32,
    class_mode="categorical",
    shuffle=True,
    seed=42
)


# In[21]:


from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv3D, MaxPooling3D, Flatten, Dense, Dropout, TimeDistributed, GRU
from keras.optimizers import Adam

def build_CNN(shape=(250, 150, 3)):
    model = Sequential([
        Conv3D(32, (3, 5, 5), padding='same', activation='relu',
               input_shape=shape),
        MaxPooling3D(),
        Dropout(0.5),
        Conv3D(64, (3, 5, 5), padding='same', activation='relu'),
        MaxPooling3D(),
        Conv3D(96, (3, 5, 5), padding='same', activation='relu'),
        MaxPooling3D(),
        Dropout(0.5),
        Flatten()
    ])
    print("CNN Built successfully!")
    return model


def combine_CNN_with_GRU(shape=(250, 150, 3)):
    CNN = build_CNN()
    model = Sequential([
        TimeDistributed(CNN, input_shape=shape),
        GRU(256),
        GRU(256),
        Dense(1024, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    print("CNN & GRU built successfully!")
    return model

def compile_model(model):
    optimizer = Adam(0.001)
    model.compile(optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model


basic_model = combine_CNN_with_GRU()
compiled_model = compile_model(basic_model)


# In[ ]:




