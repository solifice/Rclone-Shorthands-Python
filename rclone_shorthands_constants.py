from enum import Enum

class Status(Enum):
    AVAILABLE = (0, "Available")
    ENABLED = (1, "Enabled")
    DISABLED = (2, "Disabled")
    
    MISSING = (-1, "Missing")
    INVALID = (-2, "Invalid")
    NOT_EXISTS = (-3, "Does not exist")
    ONLY_FILE = (-4, "File path required")
    
    def __init__(self, val, prt):
        self.val = val
        self.prt = prt


from colorama import init, Fore, Style

SPACE = ' '

CONFIG = "_configurations"

BISYNC_WORKING_DIR = "bisync_working_directory"

CONF = "conf_files"

RCLONE_EXE_DIR = "rclone_executable_files"

RCLONE_EXE_FILE = "rclone"

GLOBAL_FILE_TXT = "global_configurations.txt"

STATUS = f"{Fore.YELLOW}STATUS:{SPACE * 3}{Style.RESET_ALL}"

RC_EXE = "Rclone Executable: "

P_MODE = f"{SPACE * 14}Portable Mode: "

P_MODE_KEY = "portableMode"

P_MODE_PROMPT = "\n> Do you want to use Portable Mode? (Y/N): "

CF_PATH = f"{SPACE * 13}Conf File Path: "

CF_PATH_KEY = "confFilePath"

CONF_EXTENSION = ".conf"

STATUS_ERROR = f"{Fore.YELLOW}Status Variables contain Errors, please fix them before proceeding...{Style.RESET_ALL}"

MAIN_MENU = (f"{Fore.LIGHTCYAN_EX}[E] | Edit Global Configurations\n"
             f"[C] | Compatibility Mode\n"
             f"[R] | Refresh\n"
             f"[0] | Exit{Style.RESET_ALL}\n\n"
             f"{Fore.YELLOW}Profile Commands{Style.RESET_ALL}\n"
             f"-----------------\n"
             f"[1] | Sync\n"
             f"[2] | Bisync\n"
             f"[3] | Copy\n"
             f"[4] | Delete\n\n"
             f"{Fore.YELLOW}Onetime Commands{Style.RESET_ALL}\n"
             f"-----------------\n"
             f"[5] | Sync\n"
             f"[6] | Bisync\n"
             f"[7] | Copy\n"
             f"[8] | Delete\n"
             f"[9] | Manual Mode")
             
TYPE_OPTION = f"Type Option: "

EGC_HEAD = "Edit Global Configurations"

EGC_NOTE = f"{Fore.LIGHTRED_EX}Note: {Fore.YELLOW}Pressing Enter without any input will skip updation...{Style.RESET_ALL}"

YES = "y"

NO = "n"

CREATE = "Creating "

CREATE_DIR = f"{CREATE}Directory {{}}"

CREATE_FILE = f"{CREATE}File {{}}"

TRUE_VALUES = ("y", "")

WINDOWS = f"{Fore.CYAN}Windows{Style.RESET_ALL}"

LINUX = f"{Fore.CYAN}Linux{Style.RESET_ALL}"

MACOS = f"{Fore.CYAN}MacOS{Style.RESET_ALL}"

SHELLS = {'bash':'Bash', 'fish':'Fish', 'ksh':'Korn', 'zsh':'Zsh', 'csh':'Csh', 'dash':'Dash', 'pwsh':'Powershell', 'elvish':'Elvish'}

CF_PATH_PROMPT = ("Select a Rclone conf file :- ", f"No conf files were found, copy-paste your conf file to {{}} and press R to refresh, press any other key to skip...", "skipping update", f"Conf files were found, Select your desired file, You can copy-paste your file to {{}} and press R to refresh, your new conf will be visible", "No selection was made, skipping update")