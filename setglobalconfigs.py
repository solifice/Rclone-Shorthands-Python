from input_output_file_operations import InputOutputFileOperations
import os
import time
import profilesync
from path_manager import PathManager
from file_folder_manager import FileFolderManager
from menu import Menu
import common_utilities as cu
import rclone_shorthands_constants as cst

#------------------------------------------------------------------------------------
    
def checkStatus(ffm, portableModeValue, confFilePathValue):
    if portableModeValue != None:
        if portableModeValue.lower() in (cst.YES, cst.NO):
            if portableModeValue.lower() == cst.YES:
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
    status_output = cst.STATUS
    error_occured = 0
    if ffm.is_file_present(rcloneFilePath) or ffm.is_file_present(rcloneFilePath+".exe") and ffm.is_file_present(rcloneFilePath+".1"):
        status_output += f"{cst.RC_EXE}{cst.AVAILABLE}"
    else:
        status_output += f"{cst.RC_EXE}{cst.MISSING}"
        error_occured += 1
        
    status_output += "\n"

    if checkStatus(ffm, portableModeValue, confFilePathValue) == -2:
        status_output += f"{cst.P_MODE}{cst.ENABLED}\n{cst.CF_PATH}{cst.MISSING}"
        error_occured += 1
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 2:
        status_output += f"{cst.P_MODE}{cst.ENABLED}\n{cst.CF_PATH}{cst.FILE_NOT_EXISTS}"
        error_occured += 1
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 3:
        status_output += f"{cst.P_MODE}{cst.ENABLED}\n{cst.CF_PATH}{cst.AVAILABLE}"
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 1:
        status_output += f"{cst.P_MODE}{cst.DISABLED}"
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == -1:
        status_output += f"{cst.P_MODE}{cst.INVALID}"
        error_occured += 1
    elif checkStatus(ffm, portableModeValue, confFilePathValue) == 0:
        status_output += f"{cst.P_MODE}{cst.MISSING}"
        error_occured += 1
       
    if error_occured:
        status_output += f"\n{menu.print_hyphen()}\n{cst.STATUS_ERROR}"
    print(menu.print_header(status_output))
    return error_occured

#------------------------------------------------------------------------------------

def main():
    pm = PathManager()
    ffm = FileFolderManager()
    menu = Menu()

    configPath = pm.create_path(cst.CONFIG, "")
    rclonePath = pm.create_path(cst.CONFIG, cst.RCLONE_EXE_DIR)
    globalFilePath = pm.create_path(cst.CONFIG, cst.GLOBAL_FILE_TXT)
    confPath = pm.create_path(cst.CONFIG, cst.CONF)
    biwdPath = pm.create_path(cst.CONFIG, cst.BISYNC_WORKING_DIR)
    rcloneFilePath = pm.create_path(rclonePath, cst.RCLONE_EXE_FILE)
    
    iofo1 = InputOutputFileOperations(globalFilePath, cst.P_MODE_KEY, cst.P_MODE_PROMPT, "")
    iofo2 = InputOutputFileOperations(globalFilePath, cst.CF_PATH_KEY, cst.CF_PATH_PROMPT.format(confPath), cst.CONF_EXTENSION)

    isFirstRun = False
    portableModeValue = None
    confFilePathValue = None
    choice = ""

    cu.clear_screen()

    if not ffm.is_dir_present(configPath):
        ffm.create_dir(configPath)
        print(cst.CREATE_DIR.format(cst.CONFIG))
        
    if not ffm.is_dir_present(rclonePath):
        ffm.create_dir(rclonePath)
        print(cst.CREATE_DIR.format(cst.RCLONE_EXE_DIR))
        
    if not ffm.is_file_present(globalFilePath):
        ffm.create_file(globalFilePath)
        print(cst.CREATE_FILE.format(cst.GLOBAL_FILE_TXT))
        isFirstRun = True
        
    if isFirstRun:
        print("\nSetting up for First Run")
        print("Starting...")
        time.sleep(5)
        choice = "e"
        
    portableModeValue = iofo1.get_value_from_file()
    if portableModeValue != None and portableModeValue.lower() == cst.YES:
        confFilePathValue = iofo2.get_value_from_file()
        
    while choice.lower() != "0":
        if choice.lower() != "e":
            cu.clear_screen()
            errorValue = printStatus(ffm, portableModeValue, confFilePathValue, rcloneFilePath)
            print(f"\n{cst.MAIN_MENU}")
            choice = input(f"\n{cst.TYPE_OPTION}")
            choice = choice.lower()

        if choice == "e":
            cu.clear_screen()
            print(f"{menu.print_header(cst.EGC_HEAD)}\n\n{cst.EGC_NOTE}")
            portableModeValue = iofo1.get_value_from_user(portableModeValue)
            iofo1.put_value_to_file(portableModeValue)
            portableModeValue = iofo1.get_value_from_file()
            if portableModeValue != None and portableModeValue.lower() == cst.YES:
                if not ffm.is_dir_present(confPath):
                    ffm.create_dir(confPath)
                if not ffm.is_dir_present(biwdPath):
                    ffm.create_dir(biwdPath)
                confFilePathValue = iofo2.get_selection_from_user(confPath)
                iofo2.put_value_to_file(confFilePathValue)
                confFilePathValue = iofo2.get_value_from_file()
            elif portableModeValue != None and portableModeValue.lower() == cst.NO:
                confFilePathValue = None
            choice = ""
        elif choice == "r":
            portableModeValue = iofo1.get_value_from_file()
            if portableModeValue != None and portableModeValue.lower() == cst.YES:
                confFilePathValue = iofo2.get_value_from_file()
        elif choice == "1":
            if errorValue == 0:
                profilesync.main()
                

if __name__ == '__main__':
    main()