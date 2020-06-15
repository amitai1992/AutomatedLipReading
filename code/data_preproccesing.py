import json
import cv2
import os


def get_video_files():  # get the names of the video files to a list
    video_files = list()
    path_to_video = 'D:/פרוייקט גמר/lombardgrid/front'  # url to dir where the dataset video locate
    for file in os.listdir(path_to_video):
        if file.endswith('mov'):  # if file end with mov add it to the list
            video_files.append(file)
    return video_files


def get_json_files():  # get the jason files to a list
    jason_files = list()
    path_to_jason_files = 'D:/פרוייקט גמר/lombardgrid/alignment'  # url path for the text of the dataset
    for pos_json in os.listdir(path_to_jason_files):  # loop at the dir and look for jason flies
        if pos_json.endswith('.json'):
            jason_files.append(pos_json)
    return jason_files


def get_video_text(jason_list, videofile):
    video_name = videofile.replace('.mov', '.json')  # name of the jason file
    jason_data = ''
    url = 'D:/פרוייקט גמר/lombardgrid/alignment'  # location of the file
    for file in jason_list:
        if file == video_name:  # if file name as the name of the video then open it as jason file
            with open('D:/פרוייקט גמר\lombardgrid/alignment/' + video_name) as json_file:
                jason_data = json.load(json_file)  # jason_data is now a jason file
                break
    return jason_data


video_files = get_video_files()
print(video_files[0])
cap = cv2.VideoCapture('D:/פרוייקט גמר/lombardgrid/front/' + video_files[0])  # get the video file
cap.set(cv2.CAP_PROP_POS_MSEC, 870)  # start from 0.87
count = 0  # number of the frame
constant = 166.6666667  # number of melsec/100 to add to get the requested 3 frames
json_files = get_json_files()  # get all the texts
print(json_files)
data = get_video_text(json_files, video_files[0])
print(data)

while (cap.isOpened()):
    ret, frame = cap.read() # read the frame
    if ret == True and cap.get(cv2.CAP_PROP_POS_MSEC) <= 1160 + constant: # play from time of 1.23 second to 1.6 second
        cv2.imshow('frame', frame) # show video
        cv2.waitKey(50)
        cv2.imwrite('frame%d.jpg' % count, frame) # save the current frame as framenumber.jpg
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    count += 1

#  Release everything if job is finished
cap.release()
cv2.destroyAllWindows()

