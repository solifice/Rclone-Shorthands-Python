import globalfunctions
import glob
import os
import time
from colorama import init, Fore, Style

#------------------------------------------------------------------------------------
def chooseFile(folder_path, extension, message):
    while True:
        input(message)
        files = glob.glob(folder_path + '/*' + extension)
        if not files:
            print(f"\n{Fore.LIGHTRED_EX}No {extension} files found at ({Fore.LIGHTCYAN_EX}{folder_path}{Fore.LIGHTRED_EX}), Make sure you have copied to correct location.{Style.RESET_ALL}")
            continue
        print(f"\n\nSelect a {extension} file:")
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
    
def checkStatus(portableModeValue, confFilePathValue):
    if portableModeValue != None:
        if portableModeValue.lower() in ("y", "n"):
            if portableModeValue.lower() == "y":
                if confFilePathValue != None and globalfunctions.isFilePresent(confFilePathValue):
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
        
def printStatus(portableModeValue, confFilePathValue, rcloneFilePath):
    errorOccured=0
    status_output = separator("=") + "\n"
    init()
    status_output += Fore.YELLOW + "STATUS:   " + Style.RESET_ALL
    error_occured = 0

    if globalfunctions.isFilePresent(rcloneFilePath) or globalfunctions.isFilePresent(rcloneFilePath+".exe") and globalfunctions.isFilePresent(rcloneFilePath+".1"):
        status_output += "Rclone Executable: "+ Fore.GREEN + "Available"+ " " * 3 + Style.RESET_ALL + "\n"
    else:
        status_output += "Rclone Executable: "+ Fore.RED + "Missing"+ " " * 3 + Style.RESET_ALL + "\n"
        error_occured += 1

    if checkStatus(portableModeValue, confFilePathValue) == -2:
        status_output += " " * 10 + "Portable Mode: " + Fore.GREEN + "Enabled" + " " * 3 + Style.RESET_ALL + "\n" + " " * 10 + "Conf File Path: " + Fore.RED + "Missing" + Style.RESET_ALL + "\n"
        error_occured += 1
    elif checkStatus(portableModeValue, confFilePathValue) == 2:
        status_output += " " * 10 + "Portable Mode: " + Fore.GREEN + "Enabled" + " " * 3 + Style.RESET_ALL + "\n" + " " * 10 + "Conf File Path: " + Fore.RED + "File does not exist" + Style.RESET_ALL + "\n"
        error_occured += 1
    elif checkStatus(portableModeValue, confFilePathValue) == 3:
        status_output += " " * 10 + "Portable Mode: " + Fore.GREEN + "Enabled" + " " * 3 + Style.RESET_ALL + "\n" + " " * 10 + "Conf File Path: " + Fore.GREEN + "Available" + Style.RESET_ALL + "\n"
    elif checkStatus(portableModeValue, confFilePathValue) == 1:
        status_output += " " * 10 + "Portable Mode: " + Fore.YELLOW + "Disabled" + Style.RESET_ALL + "\n"
    elif checkStatus(portableModeValue, confFilePathValue) == -1:
        status_output += " " * 10 + "Portable Mode: " + Fore.RED + "Invalid" + Style.RESET_ALL + "\n"
        error_occured += 1
    elif checkStatus(portableModeValue, confFilePathValue) == 0:
        status_output += " " * 10 + "Portable Mode: " + Fore.RED + "Missing" + Style.RESET_ALL + "\n"
        error_occured += 1
    if error_occured:
        status_output += "\n" + separator("-")
        status_output += "\n" + Fore.YELLOW + "Status Variables contain Errors, please fix them before proceeding..." + Style.RESET_ALL + "\n"
    status_output += separator("=")
    print(status_output)
        
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

    configPath = globalfunctions.createPath(config, "")
    rclonePath = globalfunctions.createPath(config, rclone)
    globalFilePath = globalfunctions.createPath(config, globalFile)
    confPath = globalfunctions.createPath(config, conf)
    biwdPath = globalfunctions.createPath(config, bisync_wkdir)
    rcloneFilePath = globalfunctions.createPath(rclonePath, rcloneExe)

    isFirstRun = False
    portableModeValue = None
    confFilePathValue = None
    choice = ""

    clearScreen()

    if not globalfunctions.isDirPresent(configPath):
        globalfunctions.createDir(configPath)
        print("Creating Folder "+config)
        
    if not globalfunctions.isDirPresent(rclonePath):
        globalfunctions.createDir(rclonePath)
        print("\nCreating Folder "+rclone)
        
    if not globalfunctions.isFilePresent(globalFilePath):
        globalfunctions.createFile(globalFilePath)
        print("\nCreating File "+globalFile)
        isFirstRun = True
        
    if isFirstRun:
        print("\nSetting up for First Run")
        print("Starting...")
        time.sleep(5)
        choice = "e"
        
    portableModeValue = globalfunctions.getValueFromFile(globalFilePath, "portableMode")
    if portableModeValue != None and portableModeValue.lower() == "y":
        confFilePathValue = globalfunctions.getValueFromFile(globalFilePath, "confFilePath")
        
    while choice.lower() != "0":
        if choice.lower() != "e":
            clearScreen()
            printStatus(portableModeValue, confFilePathValue, rcloneFilePath)
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
            portableModeValue = globalfunctions.getValueFromUser("portableMode", "\n> Do you want to use Portable Mode? (Y/N): ", portableModeValue)
            globalfunctions.putValueToFile(globalFilePath, "portableMode", portableModeValue)
            portableModeValue = globalfunctions.getValueFromFile(globalFilePath, "portableMode")
            if portableModeValue != None and portableModeValue.lower() == "y":
                if not globalfunctions.isDirPresent(confPath):
                    globalfunctions.createDir(confPath)
                if not globalfunctions.isDirPresent(biwdPath):
                    globalfunctions.createDir(biwdPath)
                confFilePathValue = chooseFile(confPath, ".conf", f"\n\nPlease copy-paste your .conf file at ({Fore.LIGHTCYAN_EX}{confPath}{Style.RESET_ALL})\nAfter copying, Press any key to continue...")
                globalfunctions.putValueToFile(globalFilePath, "confFilePath", confFilePathValue)
                confFilePathValue = globalfunctions.getValueFromFile(globalFilePath, "confFilePath")
            elif portableModeValue != None and portableModeValue.lower() == "n":
                confFilePathValue = None
            choice = ""
        elif choice == "r":
            portableModeValue = globalfunctions.getValueFromFile(globalFilePath, "portableMode")
            if portableModeValue != None and portableModeValue.lower() == "y":
                confFilePathValue = globalfunctions.getValueFromFile(globalFilePath, "confFilePath")
                

if __name__ == '__main__':
    main()