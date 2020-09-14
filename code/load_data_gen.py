import os

t = 'a'
# t = chr(ord(t) + 1)


arr = list()
count = 0
while(count < 27):
    arr.append(t)
    t = chr(ord(t) + 1)
    count += 1

def createFolders():
    dircetory = 'final_dataset'
    parent_dir = 'D:\lip reading final project\lombardgrid'
    path = os.path.join(parent_dir, dircetory)
    for letter in arr:
        pathDirName = os.path.join(path, letter)
        os.makedirs(pathDirName)
        print('directory ' + letter + ' created')


createFolders()