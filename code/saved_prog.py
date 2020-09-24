#first part - to start sageMaker and config the vars

from sagemaker import get_execution_role 
import tensorflow as tf
from keras_preprocessing import image
from keras_preprocessing.image import ImageDataGenerator

role = get_execution_role() 

bucket = 'letters-dataset' 
data_key = 'lettersdataset/train/1000a' 
data_location = 's3://{}/{}'.format(bucket, data_key)


#second part - declaring a function to use boto3 to download a whole folder from s3

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
        target = obj.key if local_dir is None \
            else os.path.join(local_dir, os.path.basename(obj.key))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        bucket.download_file(obj.key, target)


# third part - calling the function we declared