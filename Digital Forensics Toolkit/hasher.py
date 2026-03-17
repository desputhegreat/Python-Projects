# Modules
import os
import hashlib
import json

# Ask user whether to create baseline or verify
mode = input("Do you want to 'create' hash or 'verify' hash: ").lower().strip()

# Dictionary to store file paths and their hashes
hash_data = {}

# Validate mode input
while True:
    if mode == 'create' or mode == 'verify':
        break
    else:
        mode = input("Invalid Choice. Please try again (create/verify): ").lower().strip()


# Function to calculate SHA256 hash of a file (chunk-based for large files)
def calculate_hash(file_path):
    try: 
        with open(file_path, "rb") as file:
            sha256 = hashlib.sha256()

            # Read file in 4KB chunks to avoid loading entire file into memory
            while chunk := file.read(4096):
                sha256.update(chunk)

            return sha256.hexdigest()
    except (FileNotFoundError):
        return None

# Function to validate file or folder paths
def validate_path(path, type_expected, allow_both=0):

    # If only file OR folder is expected
    if allow_both == 0:

        # Folder validation
        if type_expected == "folder":
            while True:
                if os.path.isdir(path):
                    break
                else:
                    path = input("Invalid Directory. Please try again: ")

        # File validation
        if type_expected == "file":
            while True:
                if os.path.isfile(path):
                    break
                else:
                    path = input("Invalid File. Please try again: ")

    # If either file OR folder is allowed
    else:
        while True:
            if os.path.exists(path):
                break
            else:
                path = input("Invalid Path. Please try again: ")

    return path


# CREATE MODE
if mode == 'create':

    # Ask where to save the hash file
    output_directory = validate_path(
        input("Enter the directory where hashes will be saved: "),
        "folder"
    )

    # Path of JSON file
    json_file_path = os.path.join(output_directory, "hash.json")

    # Ask which file/folder to hash
    target_path = validate_path(
        input("Enter the directory of the file/folder to be hashed: "),
        None,
        1
    )

    # If target is a single file
    if os.path.isfile(target_path):
        file_hash = calculate_hash(target_path)
        hash_data[target_path] = file_hash

    # If target is a folder (recursive scan)
    else:
        for current_root, _, files in os.walk(target_path):
            for file_name in files:
                full_file_path = os.path.join(current_root, file_name)
                file_hash = calculate_hash(full_file_path)
                hash_data[full_file_path] = file_hash

    # Save dictionary as JSON
    with open(json_file_path, "w") as json_file:
        json.dump(hash_data, json_file, indent=4)

    print("Baseline hash file successfully created!")

# VERIFY MODE
else:
    modified_count = 0
    verified_count = 0
    deleted_count = 0
    #Ask where's the hash file
    hash_file = validate_path(input("Enter path to hash.json: "), "file", 0)
    #loading the file to data variable
    while True:    
        try:
            with open(hash_file, "r") as file:
                
                baseline_hashes = json.load(file)
            break
        except json.decoder.JSONDecodeError:
            hash_file = validate_path(input("Invalid file. Please try again: "), "file", 0)
    print("\nHere's the list of modified files:\n")
    
    #hash verifier
    for key in baseline_hashes:
        if calculate_hash(key) == baseline_hashes[key]:
            verified_count += 1
        elif calculate_hash(key) == None:
            deleted_count +=1
        else:
            print(f"{key} : Modified")    
            modified_count += 1
    #final count
    print(f"\n Total files: {len(baseline_hashes)}\n Verified Files: {verified_count}\n Modified Files: {modified_count}\n Moved/Deleted Files: {deleted_count}")