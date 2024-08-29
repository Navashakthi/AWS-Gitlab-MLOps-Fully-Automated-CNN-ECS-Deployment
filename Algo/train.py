import os
import boto3
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import zipfile
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Parameters
img_width, img_height = 64, 64
batch_size = 32
epochs = 50
num_classes = 6
s3_bucket = 'aws-bucket-name'
s3_train_data_key = 'cnn-classification/dataset/training_set.zip'
s3_validation_data_key = 'cnn-classification/dataset/test_set.zip'
s3_model_key = 'cnn-classification/output/cnn-classification-model.h5'
local_data_dir = '/opt/ml/input/data/'
train_data_dir = os.path.join(local_data_dir, 'training_set')
validation_data_dir = os.path.join(local_data_dir, 'test_set')

# Function to download and unzip data from S3
def download_and_extract_from_s3(bucket_name, s3_key, local_path):
    s3 = boto3.client('s3')
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    local_zip_path = os.path.join(local_path, 'data.zip')
    s3.download_file(bucket_name, s3_key, local_zip_path)
    with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
        zip_ref.extractall(local_path)
    os.remove(local_zip_path)

# Function to upload the model to S3
def upload_model_to_s3(model_path, bucket_name, s3_key):
    s3 = boto3.client('s3')
    s3.upload_file(model_path, bucket_name, s3_key)

# Download training and validation data
download_and_extract_from_s3(s3_bucket, s3_train_data_key, local_data_dir)
download_and_extract_from_s3(s3_bucket, s3_validation_data_key, local_data_dir)

# Data Augmentation and Preprocessing
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical'
)

validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical'
)

# Model Creation
model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(img_width, img_height, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())

model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Model Summary
model.summary()

# Model Training
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)

# Save the Model
model_path = '/opt/ml/model/cnn-classification-model.h5'
model.save(model_path)

# Upload the Model to S3
upload_model_to_s3(model_path, s3_bucket, s3_model_key)

# Evaluate the Model
loss, accuracy = model.evaluate(validation_generator)
print(f'Validation Loss: {loss}')
print(f'Validation Accuracy: {accuracy}')
