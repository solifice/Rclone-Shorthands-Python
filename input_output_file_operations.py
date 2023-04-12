from colorama import init, Fore, Style
import glob
import os

class InputOutputFileOperations:
    def __init__(self, cfg_path=None, search_dir=None, key=None, prompt_message=None, search_extension=None):
        self.cfg_path = cfg_path
        self.search_dir = search_dir
        self.key = key
        self.prompt_message = prompt_message
        self.search_extension = search_extension
        self.value = None
      
    def read_from_file(self):
        try:
            with open(self.cfg_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if self.key in line:
                        fetched_value = line.split('=')[1].strip()
                        if fetched_value == '':
                            self.value = None
                        else:
                            self.value = fetched_value
        except FileNotFoundError:
            pass
        
    def write_to_file(self):
        if self.value != None:
            try:
                with open(self.cfg_path, 'r') as f:
                    lines = f.readlines()

                is_key_present = False
                for i, line in enumerate(lines):
                    if line.startswith(self.key + '='):
                        lines[i] = f"{self.key}={self.value}\n"
                        is_key_present = True
                        break
                if not is_key_present:
                    lines.append(f"{self.key}={self.value}\n")

                with open(self.cfg_path, 'w') as f:
                    f.writelines(lines)

            except Exception as e:
                print(f"Error writing to file: {e}")

    def input_from_user(self):
        user_value = input(self.prompt_message)
        if user_value.strip() == '':
            print(f"{Fore.LIGHTYELLOW_EX}  You didn't provide any value, Skipping.{Style.RESET_ALL}")
        else:
            self.value = user_value.strip()
            
    def user_selection_from_list(self):
        while True:
            input(self.prompt_message)
            files = glob.glob(self.search_dir + '/*' + self.search_extension)
            if not files:
                print(f"\n{Fore.LIGHTRED_EX}No {self.search_extension} files found at ({Fore.LIGHTCYAN_EX}{self.search_dir}{Fore.LIGHTRED_EX}), Make sure you have copied to correct location.{Style.RESET_ALL}")
                continue
            print(f"\n\nSelect a {self.search_extension} file:")
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
