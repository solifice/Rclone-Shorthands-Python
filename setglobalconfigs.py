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

    configPath = pm.join_rcstool_path(cst.CONFIG)
    rclonePath = pm.join_custom_path(configPath, cst.RCLONE_EXE_DIR)
    globalFilePath = pm.join_custom_path(configPath, cst.GLOBAL_FILE_TXT)
    confPath = pm.join_custom_path(configPath, cst.CONF)
    biwdPath = pm.join_custom_path(configPath, cst.BISYNC_WORKING_DIR)
    rcloneFilePath = pm.join_custom_path(rclonePath, cst.RCLONE_EXE_FILE)
    
    iofo1 = InputOutputFileOperations(cfg_path=globalFilePath, key=cst.P_MODE_KEY, prompt_message=cst.P_MODE_PROMPT)
    iofo2 = InputOutputFileOperations(cfg_path=globalFilePath, search_dir=confPath, key=cst.CF_PATH_KEY, prompt_message=cst.CF_PATH_PROMPT.format(confPath), search_extension=cst.CONF_EXTENSION)

    isFirstRun = False
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
        input("Press any key to continue...")
        choice = "e"
        
    iofo1.read_from_file()
    if iofo1.checkValue() and iofo1.getValue().lower() == cst.YES:
        iofo2.read_from_file()
        
    while choice.lower() != "0":
        if choice.lower() != "e":
            cu.clear_screen()
            errorValue = printStatus(ffm, iofo1.getValue(), iofo2.getValue(), rcloneFilePath)
            print(f"\n{cst.MAIN_MENU}")
            choice = input(f"\n{cst.TYPE_OPTION}")
            choice = choice.lower()

        if choice == "e":
            cu.clear_screen()
            print(f"{menu.print_header(cst.EGC_HEAD)}\n\n{cst.EGC_NOTE}")
            iofo1.input_from_user()
            iofo1.write_to_file()
            iofo1.read_from_file()
            if iofo1.checkValue() and iofo1.getValue().lower() == cst.YES:
                if not ffm.is_dir_present(confPath):
                    ffm.create_dir(confPath)
                if not ffm.is_dir_present(biwdPath):
                    ffm.create_dir(biwdPath)
                iofo2.user_selection_from_list()
                iofo2.write_to_file()
                iofo2.read_from_file()
            print("\n\nPress any key to return to the main menu...", end="")
            cu.get_char_input()
            choice = ""
        elif choice == "r":
            iofo1.read_from_file()
            if iofo1.checkValue() and iofo1.getValue().lower() == cst.YES:
                iofo2.read_from_file()
        elif choice == "1":
            if errorValue == 0:
                profilesync.main(pm)
                

if __name__ == '__main__':
    main()