import os
import shutil

#takes folder path
while True:
    folder = input("Enter Folder Path: ")
    if os.path.isdir(folder):
        break
    else:
        folder = input("Invalid Path. Try Again: ")

files = os.listdir(folder)

extension_list = {
    'Images' : ["apng", "png", "avif", "gif", "jpg", "jpeg", "jfif", "pjpeg", "pjp", "svg", "webp", "bmp", "ico", "cur", "tif", "tiff"],
    
    'Videos' : ["mp4", "m4v", "avi", "mov", "wmv", "flv", "webm", "mpeg", "mpg", "3gp", "3g2", "vob", "mkv", "ts"],

    'Excel' : ["xls", "xlsx", "xlsm", "xlsb", "csv", "ods"],

    'Documents' : ["doc", "docx", "docm", "dotx", "dotm", "rtf", "txt", "pdf", "odt", "pages"],
    'Others' : []  
      }

#creates folders
for key in extension_list:
    try:   
        os.mkdir(f"{folder}/{key}")
    except FileExistsError:
        pass        
#finds extension and name
def extension_finder(x):
    if x.count(".") != 0:
        name, *rest = x.split('.')
        rest.reverse()
        return rest[0].lower()
    else:
        return None
#sorts compatible files
def sorter(x,y):
    file_path = f"{folder}/{x}"
    
    for key in extension_list:
        if y != None and y in extension_list[key]:
            shutil.move(file_path, f"{folder}/{key}/{x}")
            break
        else: 
            pass  
#sorts non-compatible files
def sort_others():
    for file in files:
        file_path = f"{folder}/{file}"
        if os.path.isfile(file_path):
            shutil.move(file_path, f"{folder}/Others/{file}")                   

for file in files:
    extension = extension_finder(file)
    sorter(file, extension)
files = os.listdir(folder)
sort_others()
    