import os

def is_path(path):
    return os.path.exists(path)

def is_file_present(file_path):
    if os.path.isfile(file_path):
        #print("The file", filePath, "exists.")
        return True
    else:
        #print("The file", filePath, "does not exist.")
        return False
        
def is_dir_present(folder_path):
    if os.path.isdir(folder_path):
        #print("The folder", folderPath, "exists.")
        return True
    else:
        #print("The folder", folderPath, "does not exist.")
        return False
        
def create_dir(folder_path):
    try:
        os.makedirs(folder_path)
    except OSError as e:
        print(f"Unable to create directory: {e}")

def create_file(file_path):
    try:
        with open(file_path, 'w') as f:
            pass
        #print(f"Empty file created at {filePath}")
    except Exception as e:
        print(f"Error creating file: {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        #print(f"The file '{file_path}' has been successfully deleted.")
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred while trying to delete the file '{file_path}': {e}")