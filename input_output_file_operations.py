from colorama import init, Fore, Style
import glob
import os
import time

class InputOutputFileOperations:
    def __init__(self, file_path, variable_name, prompt_message, file_extension):
        self.file_path = file_path
        self.variable_name = variable_name
        self.prompt_message = prompt_message
        self.file_extension = file_extension
      
    def get_value_from_file(self):
        try:
            with open(self.file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if self.variable_name in line:
                        variable_value = line.split('=')[1].strip()
                        if variable_value == '':
                            return None
                        variable_value = variable_value.strip()
                        return variable_value
        except FileNotFoundError:
            pass
        return None
        
    def put_value_to_file(self, variable_value):

        if variable_value != None:
            try:
                with open(self.file_path, 'r') as f:
                    lines = f.readlines()

                is_variable_present = False
                for i, line in enumerate(lines):
                    if line.startswith(self.variable_name + '='):
                        variable_value = variable_value.strip()
                        lines[i] = f"{self.variable_name}={variable_value}\n"
                        is_variable_present = True
                        break
                if not is_variable_present:
                    lines.append(f"{self.variable_name}={variable_value}\n")

                with open(self.file_path, 'w') as f:
                    f.writelines(lines)

            except Exception as e:
                print(f"Error writing to file: {e}")
                
    def get_value_from_user(self, existing_value):
        variable_value = input(self.prompt_message)
        if variable_value.strip() == '':
            print(f"{Fore.LIGHTYELLOW_EX}  You didn't provide any value, Skipping.{Style.RESET_ALL}")
            return existing_value
        return variable_value.strip()
            
    def get_selection_from_user(self, folder_path):
        while True:
            input(self.prompt_message)
            files = glob.glob(folder_path + '/*' + self.file_extension)
            if not files:
                print(f"\n{Fore.LIGHTRED_EX}No {self.file_extension} files found at ({Fore.LIGHTCYAN_EX}{folder_path}{Fore.LIGHTRED_EX}), Make sure you have copied to correct location.{Style.RESET_ALL}")
                continue
            print(f"\n\nSelect a {self.file_extension} file:")
            for i, file in enumerate(files):
                file_name = os.path.basename(file)
                print(f"{Fore.LIGHTYELLOW_EX}[{i+1}]{Style.RESET_ALL} {file_name}")
            selection = input("\nType Option: ")
            if not selection:
                print("No selection was made, skipping update")
                time.sleep(2)
                return None
            try:
                index = int(selection) - 1
                selected_file = files[index]
                return selected_file
            except (ValueError, IndexError):
                print(f"{Fore.LIGHTRED_EX}invalid selection, Try again...{Style.RESET_ALL}")
                continue