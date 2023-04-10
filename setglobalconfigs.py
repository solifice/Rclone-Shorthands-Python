from input_output_file_operations import InputOutputFileOperations
import glob
import os
import time
import profilesync
from colorama import init, Fore, Style
from path_manager import PathManager
from file_folder_manager import FileFolderManager

#------------------------------------------------------------------------------------

    
def checkStatus(ffm, portableModeValue, confFilePathValue):
    if portableModeValue != None:
        if portableModeValue.lower() in ("y", "n"):
            if portableModeValue.lower() == "y":
                if confFilePathValue != None and ffm.is_file_present(confFilePathValue):
                    return 3
                elif confFilePathValue != None:
                    return 2
                else:
                    return -2
            else:
                return 1
        else:
            return -1
    else:
        return 0
        
def printStatus(ffm, portableModeValue, confFilePathValue, rcloneFilePath):
    errorOccured=0
    status_output = separator("=") + "\n"
    init()
    status_output += Fore.YELLOW + "STATUS:   " + Style.RESET_ALL
    error_occured = 0

    if ffm.is_file_present(rcloneFilePath) or ffm.is_file_present(rcloneFilePath+".exe") and ffm.is_file_present(rcloneFilePath+".1"):
        status_output += "Rclone Executable: "+ Fore.GREEN + "Available"+ " " * 3 + Style.RESET_ALL + "\n"
    else:
        status_output += "Rclone Executable: "+ Fore.RED + "Missing"+ " " * 3 + Style.RESET_ALL + "\n"
        error_occured += 1

    if checkStatus(ffm, portableModeValue, confFilePathValue) == -2:
        status_output += " " * 10 + "Portable Mode: " + Fore.GREEN + "Enabled" + " " * 3 + Style.RESET_ALL + "\n" + " " * 10 + "Conf File Path: " + Fore.RED + "Missing" + Style.RESET_ALL + "\n"
        error_occured += 1
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 2:
        status_output += " " * 10 + "Portable Mode: " + Fore.GREEN + "Enabled" + " " * 3 + Style.RESET_ALL + "\n" + " " * 10 + "Conf File Path: " + Fore.RED + "File does not exist" + Style.RESET_ALL + "\n"
        error_occured += 1
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 3:
        status_output += " " * 10 + "Portable Mode: " + Fore.GREEN + "Enabled" + " " * 3 + Style.RESET_ALL + "\n" + " " * 10 + "Conf File Path: " + Fore.GREEN + "Available" + Style.RESET_ALL + "\n"
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 1:
        status_output += " " * 10 + "Portable Mode: " + Fore.YELLOW + "Disabled" + Style.RESET_ALL + "\n"
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == -1:
        status_output += " " * 10 + "Portable Mode: " + Fore.RED + "Invalid" + Style.RESET_ALL + "\n"
        error_occured += 1
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 0:
        status_output += " " * 10 + "Portable Mode: " + Fore.RED + "Missing" + Style.RESET_ALL + "\n"
        error_occured += 1
    if error_occured:
        status_output += "\n" + separator("-")
        status_output += "\n" + Fore.YELLOW + "Status Variables contain Errors, please fix them before proceeding..." + Style.RESET_ALL + "\n"
    status_output += separator("=")
    print(status_output)
    return error_occured
        
def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def separator(symbol):
    terminal_width = os.get_terminal_size().columns
    return symbol * (int)(terminal_width/1.2)


#------------------------------------------------------------------------------------

def main():
    config = "_config_"
    bisync_wkdir = "_bisync_wkdir_"
    conf = "_conf_"
    rclone= "_rclone_"
    globalFile = "_global_Config_.txt"
    rcloneExe = "rclone"
    
    pm = PathManager()
    ffm = FileFolderManager()

    configPath = pm.create_path(config, "")
    rclonePath = pm.create_path(config, rclone)
    globalFilePath = pm.create_path(config, globalFile)
    confPath = pm.create_path(config, conf)
    biwdPath = pm.create_path(config, bisync_wkdir)
    rcloneFilePath = pm.create_path(rclonePath, rcloneExe)
    
    iofo1 = InputOutputFileOperations(globalFilePath, "portableMode", "\n> Do you want to use Portable Mode? (Y/N): ", "")
    iofo2 = InputOutputFileOperations(globalFilePath, "confFilePath", f"\n\nPlease copy-paste your .conf file at ({Fore.LIGHTCYAN_EX}{confPath}{Style.RESET_ALL})\nAfter copying, Press any key to continue...", ".conf")

    isFirstRun = False
    portableModeValue = None
    confFilePathValue = None
    choice = ""

    clearScreen()

    if not ffm.is_dir_present(configPath):
        ffm.create_dir(configPath)
        print("Creating Folder "+config)
        
    if not ffm.is_dir_present(rclonePath):
        ffm.create_dir(rclonePath)
        print("\nCreating Folder "+rclone)
        
    if not ffm.is_file_present(globalFilePath):
        ffm.create_file(globalFilePath)
        print("\nCreating File "+globalFile)
        isFirstRun = True
        
    if isFirstRun:
        print("\nSetting up for First Run")
        print("Starting...")
        time.sleep(5)
        choice = "e"
        
    portableModeValue = iofo1.get_value_from_file()
    if portableModeValue != None and portableModeValue.lower() == "y":
        confFilePathValue = iofo2.get_value_from_file()
        
    while choice.lower() != "0":
        if choice.lower() != "e":
            clearScreen()
            errorValue = printStatus(ffm, portableModeValue, confFilePathValue, rcloneFilePath)
            mainMenu = (f"\n{Fore.LIGHTCYAN_EX}[E] | Edit Global Configurations\n"
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
                      f"[9] | Manual Mode\n")
            print(mainMenu)
            choice = input("\nType Option:")

            choice = choice.lower()

        if choice == "e":
            clearScreen()
            print(separator("="))
            print("Edit Global Configurations")
            print(separator("=")+"\n")
            print(f"{Fore.LIGHTRED_EX}Note: {Fore.YELLOW}Pressing Enter without any input will skip updation...{Style.RESET_ALL}")
            portableModeValue = iofo1.get_value_from_user(portableModeValue)
            iofo1.put_value_to_file(portableModeValue)
            portableModeValue = iofo1.get_value_from_file()
            if portableModeValue != None and portableModeValue.lower() == "y":
                if not ffm.is_dir_present(confPath):
                    ffm.create_dir(confPath)
                if not ffm.is_dir_present(biwdPath):
                    ffm.create_dir(biwdPath)
                confFilePathValue = iofo2.get_selection_from_user(confPath)
                iofo2.put_value_to_file(confFilePathValue)
                confFilePathValue = iofo2.get_value_from_file()
            elif portableModeValue != None and portableModeValue.lower() == "n":
                confFilePathValue = None
            choice = ""
        elif choice == "r":
            portableModeValue = iofo1.get_value_from_file()
            if portableModeValue != None and portableModeValue.lower() == "y":
                confFilePathValue = iofo2.get_value_from_file()
        elif choice == "1":
            if errorValue == 0:
                profilesync.main()
                

if __name__ == '__main__':
    main()