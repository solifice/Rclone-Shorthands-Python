import os

class FileFolderManager:
    def is_path(self, path):
        return os.path.exists(path)

    def is_file_present(self, file_path):
        if os.path.isfile(file_path):
            #print("The file", filePath, "exists.")
            return True
        else:
            #print("The file", filePath, "does not exist.")
            return False
            
    def is_dir_present(self, folder_path):
        if os.path.isdir(folder_path):
            #print("The folder", folderPath, "exists.")
            return True
        else:
            #print("The folder", folderPath, "does not exist.")
            return False
            
    def create_dir(self, folder_path):
        try:
            os.makedirs(folder_path)
        except OSError as e:
            print(f"Unable to create directory: {e}")

    def create_file(self, file_path):
        try:
            with open(file_path, 'w') as f:
                pass
            #print(f"Empty file created at {filePath}")
        except Exception as e:
            print(f"Error creating file: {e}")