#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sagemaker import get_execution_role 


role = get_execution_role() 

bucket = 'lipreading-dataset' 
data_key = 'alignment' 
local = 'alignment'
data_location = 's3://{}/{}'.format(bucket, data_key)


# In[25]:


import boto3
import os
s3 = boto3.resource('s3') # assumes credentials & configuration are handled outside python in .aws directory or environment variables

def download_s3_folder(bucket_name, s3_folder, local_dir):
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

