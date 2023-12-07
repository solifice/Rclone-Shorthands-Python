from colorama import init, Fore, Style
from enum import Enum


class Status(Enum):
    AVAILABLE_FILE = (0, f"{Fore.GREEN}Available{Style.RESET_ALL}")
    AVAILABLE_DIRECTORY = (3, f"{Fore.GREEN}Available{Style.RESET_ALL}")
    AVAILABLE_VALUE = (4, f"{Fore.GREEN}Available{Style.RESET_ALL}")
    ENABLED = (1, f"{Fore.GREEN}Enabled{Style.RESET_ALL}")
    DISABLED = (2, f"{Fore.YELLOW}Disabled{Style.RESET_ALL}")

    MISSING = (-1, f"{Fore.RED}Missing{Style.RESET_ALL}")
    INVALID = (-2, f"{Fore.RED}Invalid{Style.RESET_ALL}")
    NOT_EXISTS = (-3, f"{Fore.RED}Does not exist{Style.RESET_ALL}")

    def __init__(self, val, prt):
        self.val = val
        self.prt = prt


class CMDFlags(Enum):
    CLEAR_SCREEN = (
        1, "clrscr", f"[{Fore.YELLOW}Running clear screen mode{Fore.LIGHTCYAN_EX}]", 5)
    PAUSE = (
        2, "pause", f"[{Fore.YELLOW}Running pause mode{Fore.LIGHTCYAN_EX}]", 6)
    BOTH = (
        3, "both", f"[{Fore.YELLOW}Running both clear screen and pause mode{Fore.LIGHTCYAN_EX}]", 7)
    COMPAT_OFF = (0, "", "[Use this if facing any terminal gliches]", 8)

    def __init__(self, val, arg, prt, returncode):
        self.val = val
        self.arg = arg
        self.prt = prt
        self.returncode = returncode


class DataType(Enum):
    PATH = "path"
    LOCAL_PATH = "local path"
    YESNO = "yesno"
    STRING = "string"


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
             f"[C] | Compatibility Mode {{}}\n"
             f"[R] | Refresh\n"
             f"[0] | Exit{Style.RESET_ALL}\n\n"
             f"{Fore.YELLOW}Operations{Style.RESET_ALL}\n"
             f"-----------------\n"
             f"[1] | Sync\n"
             f"[2] | Bisync\n"
             f"[3] | Copy\n"
             f"[4] | Delete\n\n")

TYPE_OPTION = f"Select an option: "

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

SHELLS = {'bash': 'Bash', 'fish': 'Fish', 'ksh': 'Korn', 'zsh': 'Zsh',
          'csh': 'Csh', 'dash': 'Dash', 'pwsh': 'Powershell', 'elvish': 'Elvish'}

CF_PATH_PROMPT = ("Select a Rclone conf file :- ", f"No conf files were found, copy-paste your conf file to {{}} and press R to refresh, press any other key to skip...", "skipping update",
                  f"Conf files were found, Select your desired file, You can copy-paste your file to {{}} and press R to refresh, your new conf will be visible", "No selection was made, skipping update")

SKIP_USER_INPUT = f"{Fore.LIGHTYELLOW_EX}  You didn't provide any value, Skipping.{Style.RESET_ALL}"
