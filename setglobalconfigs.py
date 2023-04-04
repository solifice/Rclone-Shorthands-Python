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
            print(f"No {extension} files found in {folder_path}, Retrying...")
            continue
        print(f"Select a {extension} file:")
        for i, file in enumerate(files):
            file_name = os.path.basename(file)
            print(f"{i+1}. {file_name}")
        selection = input("> ")
        if not selection:
            print("No selection was made, skipping update")
            time.sleep(2)
            return None
        try:
            index = int(selection) - 1
            selected_file = files[index]
            return selected_file
        except (ValueError, IndexError):
            print("invalid selection, Retrying...")
            continue
    
def checkStatus(portableModeValue, confFilePathValue):
    if portableModeValue != None:
        if portableModeValue.lower() in ('true', 'false'):
            if portableModeValue.lower() == 'true':
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
        
def printStatus():
    errorOccured=0
    terminal_width = os.get_terminal_size().columns
    print("=" * (int)(terminal_width/1.2))
    init()
    print(Fore.YELLOW+"STATUS:   "+Style.RESET_ALL, end="")
    if globalfunctions.isFilePresent(rcloneFilePath) or globalfunctions.isFilePresent(rcloneFilePath+".exe") and globalfunctions.isFilePresent(rcloneFilePath+".1"):
        print("Rclone Executable: "+ Fore.GREEN + "Available"+ " " * 3 + Style.RESET_ALL)
    else:
        print("Rclone Executable: "+ Fore.RED + "Missing"+ " " * 3 + Style.RESET_ALL)
        errorOccured=+1
    if checkStatus(portableModeValue, confFilePathValue) == -2:
        print(" " * 10+"Portable Mode: " + Fore.GREEN + "Enabled" + " " * 3 + Style.RESET_ALL+"\n"+" " * 10 +"Conf File Path: " + Fore.RED + "Missing" + Style.RESET_ALL)
        errorOccured=+1
    if checkStatus(portableModeValue, confFilePathValue) == 2:
        print(" " * 10+"Portable Mode: " + Fore.GREEN + "Enabled" + " " * 3 + Style.RESET_ALL +"\n" + " " * 10 +"Conf File Path: " + Fore.RED + "File does not exist" + Style.RESET_ALL)
        errorOccured=+1
    if checkStatus(portableModeValue, confFilePathValue) == 3:
        print(" " * 10+"Portable Mode: " + Fore.GREEN + "Enabled" + " " * 3 + Style.RESET_ALL +"\n" + " " * 10 +"Conf File Path: " + Fore.GREEN + "Available" + Style.RESET_ALL)
    if checkStatus(portableModeValue, confFilePathValue) == 1:
        print(" " * 10+"Portable Mode: " + Fore.YELLOW + "Disabled"+ Style.RESET_ALL)
    if checkStatus(portableModeValue, confFilePathValue) == -1:
        print(" " * 10+"Portable Mode: " + Fore.RED + "Invalid"+ Style.RESET_ALL)
        errorOccured=+1
    if checkStatus(portableModeValue, confFilePathValue) == 0:
        print(" " * 10+"Portable Mode: " + Fore.RED + "Missing"+ Style.RESET_ALL)
        errorOccured=+1
    if errorOccured:
        print("\n"+Fore.YELLOW+"Status Variables contain Errors, please fix them before proceeding..."+Style.RESET_ALL)
    print("=" * (int)(terminal_width/1.2))
        
def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


#------------------------------------------------------------------------------------

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
if portableModeValue != None and portableModeValue.lower() == "true":
    confFilePathValue = globalfunctions.getValueFromFile(globalFilePath, "confFilePath")
    
while choice.lower() != "0":
    if choice.lower() != "e":
        clearScreen()
        printStatus()
        print("\n"+Fore.LIGHTCYAN_EX+"[E] | Edit Global Configurations")
        print("[0] | Exit")
        print("[R] | Refresh"+Style.RESET_ALL)
        print("\n\n"+Fore.YELLOW+"Profile Commands"+Style.RESET_ALL)
        print("-----------------")
        print("[1] | Sync")
        print("[2] | Bisync")
        print("[3] | Copy")
        print("[4] | Delete")
        print("\n\n"+Fore.YELLOW+"Onetime Commands"+Style.RESET_ALL)
        print("-----------------")
        print("[5] | Sync")
        print("[6] | Bisync")
        print("[7] | Copy")
        print("[8] | Delete")
        print("[9] | Manual Mode")
        choice = input("\n\nType Option:")
        choice = choice.lower()

    if choice == "e":
        os.system('cls' if os.name == 'nt' else 'clear')
        portableModeValue = globalfunctions.getValueFromUser("portableMode", "You want to use Portable Mode? (True/False) :-", portableModeValue)
        globalfunctions.putValueToFile(globalFilePath, "portableMode", portableModeValue)
        portableModeValue = globalfunctions.getValueFromFile(globalFilePath, "portableMode")
        if portableModeValue != None and portableModeValue.lower() == "true":
            if not globalfunctions.isDirPresent(confPath):
                globalfunctions.createDir(confPath)
            if not globalfunctions.isDirPresent(biwdPath):
                globalfunctions.createDir(biwdPath)
            confFilePathValue = chooseFile(confPath, ".conf", "\nPlease copy & paste your .conf file to path "+confPath+"\nAfter copying, press any key to continue...")
            globalfunctions.putValueToFile(globalFilePath, "confFilePath", confFilePathValue)
            confFilePathValue = globalfunctions.getValueFromFile(globalFilePath, "confFilePath")
        elif portableModeValue != None and portableModeValue.lower() == "false":
            confFilePathValue = None
        choice = ""
    elif choice == "r":
        portableModeValue = globalfunctions.getValueFromFile(globalFilePath, "portableMode")
        if portableModeValue != None and portableModeValue.lower() == "true":
            confFilePathValue = globalfunctions.getValueFromFile(globalFilePath, "confFilePath")