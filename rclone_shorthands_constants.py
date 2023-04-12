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

AVAILABLE = f"{Fore.GREEN}Available{Style.RESET_ALL}"

MISSING = f"{Fore.RED}Missing{Style.RESET_ALL}"

INVALID = f"{Fore.RED}Invalid{Style.RESET_ALL}"

P_MODE = f"{SPACE * 14}Portable Mode: "

P_MODE_KEY = "portableMode"

P_MODE_PROMPT = "\n> Do you want to use Portable Mode? (Y/N): "

ENABLED = f"{Fore.GREEN}Enabled{Style.RESET_ALL}"

DISABLED = f"{Fore.YELLOW}Disabled{Style.RESET_ALL}"

CF_PATH = f"{SPACE * 13}Conf File Path: "

CF_PATH_KEY = "confFilePath"

CF_PATH_PROMPT = f"\n\nPlease copy-paste your .conf file at ({Fore.LIGHTCYAN_EX}{{}}{Style.RESET_ALL})\nAfter copying, Press any key to continue..."

CONF_EXTENSION = ".conf"

FILE_NOT_EXISTS = f"{Fore.RED}File does not exist{Style.RESET_ALL}"

STATUS_ERROR = f"{Fore.YELLOW}Status Variables contain Errors, please fix them before proceeding...{Style.RESET_ALL}"

MAIN_MENU = (f"{Fore.LIGHTCYAN_EX}[E] | Edit Global Configurations\n"
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