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
    terminal_width = os.get_terminal_size().columns
    print("=" * terminal_width+ "\n")
    init()
    if checkStatus(portableModeValue, confFilePathValue) == -2:
        print("Portable Mode: " + Fore.GREEN + "ENABLED" + " " * 5 + Style.RESET_ALL +"|" + " " * 5 +"Conf File Path: " + Fore.RED + "???" + Style.RESET_ALL)
    if checkStatus(portableModeValue, confFilePathValue) == 2:
        print("confFilePath value is present but .conf file doesn't exists")
    if checkStatus(portableModeValue, confFilePathValue) == 3:
        print("Portable Mode: "+Fore.GREEN+"ENABLED"+Style.RESET_ALL)
        print(".conf file is set")
    if checkStatus(portableModeValue, confFilePathValue) == 1:
        print("Portable Mode : FALSE")
    if checkStatus(portableModeValue, confFilePathValue) == -1:
        print("portableMode value is invalid")
    if checkStatus(portableModeValue, confFilePathValue) == 0:
        print("portableMode value is missing")
        
def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


#------------------------------------------------------------------------------------

config = "_config_"
bisync_wkdir = "_bisync_wkdir_"
conf = "_conf_"
rclone= "_rclone_"
globalFile = "_global_Config_.txt"

configPath = globalfunctions.createPath(config, "")
rclonePath = globalfunctions.createPath(config, rclone)
globalFilePath = globalfunctions.createPath(config, globalFile)
confPath = globalfunctions.createPath(config, conf)
biwdPath = globalfunctions.createPath(config, bisync_wkdir)

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
    if choice != "e":
        clearScreen()
        printStatus()
        print("\n[E] Edit Global Configurations")
        print("[0] Exit")
        print("[R] Refresh")
        print("\nCommands to use with profiles")
        print("Press 1 for Sync")
        print("\nCommands to one time use")
        print("Press 1 for Sync")
        choice = input("\n\nEnter your choice :- ")

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