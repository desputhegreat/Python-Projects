import os
import shutil

while True:
    folder = input("Enter Folder Path: ")
    if os.path.isdir(folder):
        break
    else:
        folder = input("Invalid Path. Try Again: ")

files = os.listdir(folder)
folder_names = ["Images", "Videos", "Excel","Documents" , "Others"]
extension_list = {
    'Images' : ["apng", "png", "avif", "gif", "jpg", "jpeg", "jfif", "pjpeg", "pjp", "svg", "webp", "bmp", "ico", "cur", "tif", "tiff"],
    
    'Videos' : ["mp4", "m4v", "avi", "mov", "wmv", "flv", "webm", "mpeg", "mpg", "3gp", "3g2", "vob", "mkv", "ts"],

    'Excel' : ["xls", "xlsx", "xlsm", "xlsb", "csv", "ods"],

    'Document' : ["doc", "docx", "docm", "dotx", "dotm", "rtf", "txt", "pdf", "odt", "pages"]
      }

#creates folders
for name in folder_names:
    try:   
        os.mkdir(f"{folder}/{name}")
    except FileExistsError:
        pass        
#finds extension and name
def extension_finder(x):
    if x.count(".") != 0:
        name, *rest = x.split('.')
        rest.reverse()
        return (name, rest[0])
    else: 
        name, *rest = x.split('.')
        return (name, None)
#sorts compatible files
def sorter(x,y):
    file_name = f"{x}.{y}"
    file_path = f"{folder}/{file_name}"
    
    for key in extension_list:
        if y in extension_list[key]:
            shutil.move(file_path, f"{folder}/{key}/{x}.{y}")
        else: 
            pass  
#sorts non-compatible files
def sort_others(x,y):
    file_name = f"{x}.{y}"
    file_path = f"{folder}/{file_name}"

    for item in folder:
        if os.path.isfile(file_path):
            shutil.move(file_path, f"{folder}/Others/{x}.{y}")                   

for file in files:
    extension = extension_finder(file)[1]
    name = extension_finder(file)[0]
    sorter(name, extension)
    sort_others(name, extension)
    