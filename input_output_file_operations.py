from colorama import init, Fore, Style
import glob
import os

class InputOutputFileOperations:
    def __init__(self, path=None, folder_path=None, key=None, prompt_message=None, file_extension=None):
        self.path = path
        self.folder_path = folder_path
        self.key = key
        self.prompt_message = prompt_message
        self.file_extension = file_extension
        self.value = None
      
    def get_value_from_file(self):
        try:
            with open(self.path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if self.key in line:
                        file_value = line.split('=')[1].strip()
                        file_value = file_value.strip()
                        self.value = file_value
        except FileNotFoundError:
            pass
        
    def put_value_to_file(self):
        file_value = self.value
        if file_value != None:
            try:
                with open(self.path, 'r') as f:
                    lines = f.readlines()

                is_key_present = False
                for i, line in enumerate(lines):
                    if line.startswith(self.key + '='):
                        file_value = file_value.strip()
                        lines[i] = f"{self.key}={file_value}\n"
                        is_key_present = True
                        break
                if not is_key_present:
                    lines.append(f"{self.key}={file_value}\n")

                with open(self.path, 'w') as f:
                    f.writelines(lines)

            except Exception as e:
                print(f"Error writing to file: {e}")

    def get_value_from_user(self):
        file_value = input(self.prompt_message)
        if file_value.strip() == '':
            print(f"{Fore.LIGHTYELLOW_EX}  You didn't provide any value, Skipping.{Style.RESET_ALL}")
        else:
            self.value = file_value.strip()
            
    def get_selection_from_user(self):
        while True:
            input(self.prompt_message)
            files = glob.glob(self.folder_path + '/*' + self.file_extension)
            if not files:
                print(f"\n{Fore.LIGHTRED_EX}No {self.file_extension} files found at ({Fore.LIGHTCYAN_EX}{self.folder_path}{Fore.LIGHTRED_EX}), Make sure you have copied to correct location.{Style.RESET_ALL}")
                continue
            print(f"\n\nSelect a {self.file_extension} file:")
            for i, file in enumerate(files):
                file_name = os.path.basename(file)
                print(f"{Fore.LIGHTYELLOW_EX}[{i+1}]{Style.RESET_ALL} {file_name}")
            selection = input("\nType Option: ")
            if not selection:
                print("No selection was made, skipping update")
                break
            try:
                index = int(selection) - 1
                selected_file = files[index]
                self.value = selected_file
                break
            except (ValueError, IndexError):
                print(f"{Fore.LIGHTRED_EX}invalid selection, Try again...{Style.RESET_ALL}")
                continue
     
    def checkValue(self):
        return self.value != None
        
    def getValue(self):
        return self.value
