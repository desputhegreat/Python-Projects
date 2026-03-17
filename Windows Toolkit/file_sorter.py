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
    'Images': ["apng", "png", "avif", "gif", "jpg", "jpeg", "jfif", "pjpeg", "pjp", "svg", "webp", "bmp", "ico", "cur", "tif", "tiff", "psd", "ai", "eps", "raw", "cr2", "nef", "orf", "sr2"],

    'Video': ["mp4", "m4v", "avi", "mov", "wmv", "flv", "webm", "mpeg", "mpg", "3gp", "3g2", "vob", "mkv", "ts", "m2v", "m4p", "rm", "rmvb", "ogv", "qt", "swf"],

    'Audio': ["mp3", "wav", "ogg", "m4a", "flac", "aac", "wma", "alac", "aiff", "mid", "midi", "amr", "opus"],

    'Documents': ["doc", "docx", "docm", "dotx", "dotm", "rtf", "txt", "pdf", "odt", "pages", "md", "tex", "wpd", "wps", "log", "eml", "msg", "pst", "vcf", "ics"],

    'Excel': ["xls", "xlsx", "xlsm", "xlsb", "csv", "ods", "xltx", "xltm", "dif", "sxc"],

    'Presentations': ["ppt", "pptx", "pptm", "ppsx", "ppsm", "potx", "potm", "odp", "key", "pps"],

    'Compressed': ["zip", "rar", "7z", "tar", "gz", "bz2", "xz", "iso", "dmg", "cab", "jar", "war", "egg", "apk", "pkg", "deb", "rpm", "z", "tgz", "tbz2"],

    'Code': ["py", "js", "html", "htm", "css", "json", "xml", "yml", "yaml", "csv", "sql", "sh", "bash", "c", "cpp", "java", "ts", "tsx", "jsx", "rb", "php", "swift", "go", "rs", "cs", "pl", "r", "m", "v", "lua", "scala", "kt", "dart", "erl", "ex", "exs", "hs", "clj", "scala", "f", "f90"],

    'Programs': ["exe", "msi", "bat", "cmd", "sh", "bash", "pl", "py", "jar", "app", "bin", "run", "deb", "rpm", "msix", "apk"],

    'Fonts': ["ttf", "otf", "woff", "woff2", "eot", "fon", "pfb", "pfm", "afm"],

    'CAD': ["dwg", "dxf", "stp", "step", "iges", "igs", "obj", "stl", "3dm", "skp", "fbx", "max"],

    'Ebooks': ["epub", "mobi", "azw", "azw3", "fb2", "lit", "lrf", "cbz", "cbr"],

    'Others': []
}

#creates folders
#for key in extension_list:
#    try:   
#        os.mkdir(f"{folder}/{key}")
#    except FileExistsError:
#        pass        
#finds extension and name
def extension_finder(x):
    if x.count(".") != 0:
        _, *rest = x.split('.')
        rest.reverse()
        return rest[0].lower()
    else:
        return None
#sorts compatible files
def sorter(x,y):
    file_path = f"{folder}/{x}"
    
    for key in extension_list:
        if y != None and y in extension_list[key]:
            try:    
                shutil.move(file_path, f"{folder}/{key}/{x}")
                break
            except FileNotFoundError:
                os.mkdir(f"{folder}/{key}")
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
print("Successfully sorted the files!")    