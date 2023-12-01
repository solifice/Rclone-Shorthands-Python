from colorama import init, Fore, Style
import glob
import os
import rclone_shorthands_constants as cst
import file_folder_manager as ffm
import re
import subprocess

from rclone_shorthands_constants import Status

import logging

logging.basicConfig(
    # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('example.log'),  # Save logs to a file
        logging.StreamHandler()           # Print logs to the console
    ]
)


class InputOutputFileOperations:
    def __init__(self, cfg_path=None, key=None, delimiter="=", prompt_message=None, search_dir=None, search_extension=None):
        self.delimiter = delimiter
        if cfg_path is not None:
            self.cfg_path = cfg_path
        if key is not None:
            self.key = key
        if prompt_message is not None:
            self.prompt_message = prompt_message
        self.value = None
        self.status = None
        if search_dir is not None:
            self.search_dir = search_dir
        self.search_extension = search_extension

    def read_from_file(self):
        try:
            with open(self.cfg_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if self.key in line:
                        fetched_value = line.split(self.delimiter)[1].strip()
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
                    if line.startswith(self.key + self.delimiter):
                        lines[i] = f"{self.key}{self.delimiter}{self.value}\n"
                        is_key_present = True
                        break
                if not is_key_present:
                    lines.append(f"{self.key}{self.delimiter}{self.value}\n")

                with open(self.cfg_path, 'w') as f:
                    f.writelines(lines)

            except Exception as e:
                print(f"Error writing to file: {e}")

    def input_from_user(self):
        user_value = input(self.prompt_message)
        if user_value.strip() == '':
            print(
                f"{Fore.LIGHTYELLOW_EX}  You didn't provide any value, Skipping.{Style.RESET_ALL}")
        else:
            self.value = user_value.strip()

    def user_selection_from_list(self):
        print(self.prompt_message[0])
        while True:
            files = glob.glob(self.search_dir + '/*' + self.search_extension)
            if not files:
                print(self.prompt_message[1].format(self.search_dir))
                choice = input("Type Option: ")
                if choice.strip().lower() == "r":
                    continue
                print(self.prompt_message[2])
                break
            print(self.prompt_message[3].format(self.search_dir))
            for i, file in enumerate(files):
                file_name = os.path.basename(file)
                print(
                    f"{Fore.LIGHTYELLOW_EX}[{i+1}]{Style.RESET_ALL} {file_name}")
            selection = input("\nType Option: ")
            if selection.strip().lower() == "r":
                continue
            if not selection:
                print(self.prompt_message[4])
                break
            try:
                index = int(selection) - 1
                selected_file = files[index]
                self.value = selected_file
                break
            except (ValueError, IndexError):
                print(
                    f"{Fore.LIGHTRED_EX}Invalid selection, Try again...{Style.RESET_ALL}")
                continue

    def check_status(self, cu):
        if self.value is None:
            self.status = Status.MISSING
        else:
            if self.delimiter == "->":
                if self.is_path():
                    os_type = cu.get_os()
                    if os_type == cst.WINDOWS and self.final in ("wdwpc", "wde"):
                        self.is_file_folder(self.value)
                    elif os_type == cst.LINUX and self.final == "lmc":
                        self.is_file_folder(self.value)
                    elif os_type == cst.MACOS and self.final in ("lmc", "mc"):
                        self.is_file_folder(self.value)
                    elif self.final in ("rdrpc", "rde") and self.key in ("source", "destination"):
                        self.is_rc_file_folder(self.value)
                    else:
                        self.status = "Decode Success, but not present"
                else:
                    self.status = Status.INVALID
            else:
                if self.value == "y":
                    self.status = Status.ENABLED
                elif self.value == "n":
                    self.status = Status.DISABLED
                else:
                    self.status = Status.INVALID
        return self.status

    def is_rc_file_folder(self, path):
        cmd = ["rclone", os.environ.get(
            "RCLONE_CONFIG_PATH", ""), "ls", path]
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            self.status = Status.NOT_EXISTS
        else:
            cmd = ["rclone", os.environ.get(
                "RCLONE_CONFIG_PATH", ""), "rmdir", "--dry-run", path]
            newresult = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if newresult.returncode == 1:
                self.status = Status.AVAILABLE_FILE
            else:
                self.status = Status.AVAILABLE_DIRECTORY

    def is_file_folder(self, path):
        if ffm.is_file_present(path):
            self.status = Status.AVAILABLE_FILE
        elif ffm.is_dir_present(path):
            self.status = Status.AVAILABLE_DIRECTORY
        else:
            self.status = Status.NOT_EXISTS

    def getValue(self):
        return self.value

    def is_path(self):
        self.final = ""
        string = self.value
        if string.count(":") == 1:
            parts = string.split(":")
            drive = parts[0]
            path = parts[1] if len(parts) > 1 else ""
            check_drive = self.is_valid_drive(drive)
            self.final += check_drive
            if check_drive == "wd" or check_drive == "rd":
                if path != "":
                    check_path = self.is_wr_path(path, check_drive)
                    self.final += check_path
                else:
                    self.final += "e"
        elif string.count(":") == 0:
            path = string
            check_path = self.is_lm_path(path)
            self.final += check_path
        else:
            self.final += "f"
        if self.final in ("wdwpc", "wde", "rdrpc", "rde", "lmc", "mc"):
            return True
        else:
            return False

    def is_valid_name(self, path):
        invalid_names = ['CON', 'PRN', 'AUX', 'NUL']
        invalid_names += ['COM{}'.format(i) for i in range(1, 10)]
        invalid_names += ['LPT{}'.format(i) for i in range(1, 10)]
        for name in re.split(r'[\\/]', path):
            if not name:
                continue
            if any(char in name for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']):
                return "f"
            if name.upper() in invalid_names:
                return "f"
        return "c"

    def is_wr_path(self, path, check_drive):
        if check_drive == "wd":
            if path.startswith(("/", "\\")):
                return "wp" + self.is_valid_name(path)
            else:
                return "f"
        else:
            return "rp" + self.is_valid_name(path)

    def is_lm_path(self, path):
        if path.startswith(("/", "\\")):
            return "lm" + self.is_valid_name(path)
        elif path.startswith("~/") or path.startswith(os.path.splitdrive(os.path.abspath('/'))):
            return "m" + self.is_valid_name(path)
        else:
            return "f"

    def is_valid_drive(self, drive):
        if len(drive) == 0:
            return "f"
        elif len(drive) == 1:
            if drive.isalpha():
                return "wd"
            elif drive in ("_", ".") or drive.isdigit():
                return "rd"
            else:
                return "f"
        else:
            if drive.startswith("-"):
                return "f"
            for char in drive:
                if not char.isalnum() and char not in ['-', ' ', '_', '.']:
                    return "f"
            return "rd"

    def checkValue(self):
        return self.value != None
