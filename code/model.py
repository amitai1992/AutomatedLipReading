# 1.0. loop to run on all images and data points in S3 train set
# 1.1. for every folder =>
# 1.1.1. for every image => call the "save_lips_of_image" function
# 2.0. and now every folder is a data point - every image has

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

#how to combine the model with fit_generator ?