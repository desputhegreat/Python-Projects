# modules
import shutil
import os

# confirmation
print("Note: Run as Administrator for full cleaning.\n")
confirm = input("This will delete temp files. Continue? (y/n): ")

if confirm.lower() != 'y':
    print("Operation cancelled.")
    exit()
freed_space = 0
file_count = 0
folder_skipped = 0
folder_count = 0

# directories
user = os.getlogin()
folders = [
    # User temp
    f"C:/Users/{user}/AppData/Local/Temp",
    f"C:/Users/{user}/AppData/Local/CrashDumps",
    f"C:/Users/{user}/AppData/Local/Microsoft/Windows/INetCache",
    f"C:/Users/{user}/AppData/Local/Microsoft/Windows/Temporary Internet Files",

    # Windows temp
    f"C:/Windows/Temp",
    f"C:/Windows/Prefetch",

    # Software caches
    f"C:/Users/{user}/AppData/Local/Packages",

    # Recycle Bin
    f"C:/$Recycle.Bin"
]

for folder in folders:
    # path verification and listing
    try:
        files = os.listdir(folder)
    except PermissionError:
        print(f"Folder access denied, skipping: {folder}")
        folder_skipped += 1
        continue
    except FileNotFoundError:
        print(f"Folder not found, skipping: {folder}")
        folder_skipped += 1
        continue
    # verfication and deletion
    for file in files:
        file_path = os.path.join(folder, file)
        try:
            if os.path.isdir(file_path) != True:
                size = os.path.getsize(file_path)
                os.remove(file_path)
                freed_space += size
                file_count += 1
            else:
                size = os.path.getsize(file_path)
                shutil.rmtree(file_path)
                freed_space += size
                folder_count += 1
            print(f"File '{file_path}' deleted successfully.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except PermissionError:
            print(f"Permission denied to delete '{file_path}'.")
        except (OSError):
            print(f"Skipping (in use or locked): {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

print(
    f"Operation Completed.\nTotal size freed: {(freed_space/1024**2):.2f} MB\nTotal Files deleted: {file_count}\nFolder deleted: {folder_count}\nFolder skipped: {folder_skipped}")
print("Press enter to exit."), input()
