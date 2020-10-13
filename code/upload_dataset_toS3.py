#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import boto3

s3 = boto3.resource('s3')


# In[ ]:


import glob

for filepath in glob.glob('updated_dataset/**/**/*.jpg', recursive=True):
    s =  filepath.split("/")[4]
    s3.meta.client.upload_file(filepath, 'alrdataset', filepath)
    print("=>done with: ",filepath)

