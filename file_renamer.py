import os

while True:
    folder = input("Enter Folder Path: ")
    if os.path.isdir(folder):
        break
    else:
        folder = input("Invalid Path. Try Again: ")

files = os.listdir(folder)

files.sort(
    key = lambda file: os.path.getmtime(os.path.join(folder, file))
)
  
x = input("Enter the starting point of numbering: ")

ext = input("Enter extension of files to be renamed(eg: .pdf): ")

for file in files:
    if file.endswith(ext):
        op = os.path.join(folder, file)
        np = os.path.join(folder, f"SST Ch-{x}.pdf")
        os.rename(op,np)
        x += 1