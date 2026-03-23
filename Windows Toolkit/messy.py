import os
import shutil

def validator(dir, x = 0):   
    if x == 0:
        while True:
            if os.path.isfile(dir):
                return dir
            else:
                x = input("Invalid directory. Please try again: ")
    if x == 1:
        while True:
            if os.path.isdir(dir):
                return dir
            else:
                x = input("Invalid directory. Please try again: ")

target_dir = validator(input("Enter target folder directory: "), 1)

for root, _, file_names in os.walk(target_dir):
    for file in file_names:
        new_location = os.path.join(target_dir, file)
        old_location = os.path.join(root, file)
        shutil.move(old_location, new_location)
print("Successfully moved all the contents!")        