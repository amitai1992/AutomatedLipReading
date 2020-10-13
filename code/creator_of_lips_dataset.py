#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('pip', 'install imutils')
get_ipython().run_line_magic('pip', 'install dlib')


# In[ ]:


from imutils import face_utils
import numpy as np
import matplotlib.pyplot as plt
import dlib
import cv2

def save_lips_of_image(input_image_path, where_to_save_image_path,image_name):
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    predictor =  dlib.shape_predictor("lips_finder/shape_predictor_68_face_landmarks.dat")
    detector = dlib.get_frontal_face_detector()
    inter = cv2.INTER_AREA
    dim = (250, 250)

    # load the input image, resize it, and convert it to grayscale
    image = cv2.imread(input_image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale image
    rects = detector(gray, 1)
    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        # loop over the face parts individually
        for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
            # clone the original image so we can draw on it, then
            # display the name of the face part on the image
            clone = image.copy()
            cv2.putText(clone, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255), 2)
            # loop over the subset of facial landmarks, drawing the
            # specific face part
            for (x, y) in shape[i:j]:
                cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)
            # extract the ROI of the face region as a separate image
            (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
            roi = image[y:y + h, x:x + w]
            roi = cv2.resize(roi, dim, interpolation=inter)
            frame = roi.copy()
            # save the particular face part
            if not cv2.imwrite(image_name, frame):
                print("DIDNT SAVE=>",image_name)
            else:
                print("==>SAVED IMAGE IN: ",image_name)
            break


# In[ ]:


import glob

count = 0

folder_for_output = "lips_cut_dataset/"

for extern_folder in glob.glob('updated_dataset/*',recursive=True):
    for intern_folder in glob.glob(extern_folder+'/*',recursive=True):
        for letter_folder in glob.glob(intern_folder+'/*',recursive=True):
            for intern_letter_folder in glob.glob(letter_folder+'/*',recursive=True):
                count+=1
                folder_img_taken_from = intern_letter_folder.split("/")[1:]
                image_name = intern_letter_folder.split("/")[-1]
                folder_img_taken_from_as_string = "/".join(folder_img_taken_from)
                output_path = folder_for_output + folder_img_taken_from_as_string
                save_lips_of_image(intern_letter_folder, output_path,image_name)
                print("=>done with: ",output_path)

print(count)


# In[ ]:




