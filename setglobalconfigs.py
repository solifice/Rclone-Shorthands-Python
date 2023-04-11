from input_output_file_operations import InputOutputFileOperations
import os
import time
import profilesync
from colorama import init, Fore, Style
from path_manager import PathManager
from file_folder_manager import FileFolderManager
from menu import Menu
import common_utilities as cu
import RSConstants as rsc

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
    menu = Menu()
    init()
    status_output = rsc.STATUS
    error_occured = 0
    if ffm.is_file_present(rcloneFilePath) or ffm.is_file_present(rcloneFilePath+".exe") and ffm.is_file_present(rcloneFilePath+".1"):
        status_output += f"{rsc.RC_EXE}{rsc.AVAILABLE}"
    else:
        status_output += f"{rsc.RC_EXE}{rsc.MISSING}"
        error_occured += 1
        
    status_output += "\n"

    if checkStatus(ffm, portableModeValue, confFilePathValue) == -2:
        status_output += f"{rsc.P_MODE}{rsc.ENABLED}\n{rsc.CF_PATH}{rsc.MISSING}"
        error_occured += 1
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 2:
        status_output += f"{rsc.P_MODE}{rsc.ENABLED}\n{rsc.CF_PATH}{rsc.FILE_NOT_EXISTS}"
        error_occured += 1
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 3:
        status_output += f"{rsc.P_MODE}{rsc.ENABLED}\n{rsc.CF_PATH}{rsc.AVAILABLE}"
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 1:
        status_output += f"{rsc.P_MODE}{rsc.DISABLED}"
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == -1:
        status_output += f"{rsc.P_MODE}{rsc.INVALID}"
        error_occured += 1
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 0:
        status_output += f"{rsc.P_MODE}{rsc.MISSING}"
        error_occured += 1
       
    if error_occured:
        status_output += f"\n{menu.print_hyphen()}\n{rsc.STATUS_ERROR}"
    print(menu.print_header(status_output))
    return error_occured

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
    menu = Menu()

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

    cu.clear_screen()

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
            cu.clear_screen()
            errorValue = printStatus(ffm, portableModeValue, confFilePathValue, rcloneFilePath)
            print(f"\n{rsc.MAIN_MENU}")
            choice = input(f"\n{rsc.TYPE_OPTION}")
            choice = choice.lower()

        if choice == "e":
            cu.clear_screen()
            print(f"{menu.print_header(rsc.EGC_HEAD)}\n\n{rsc.EGC_NOTE}")
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