from input_output_file_operations import InputOutputFileOperations
import os
import time
import profilesync
from path_manager import PathManager
from file_folder_manager import FileFolderManager
from menu import Menu
from common_utilities import CommonUtils
import rclone_shorthands_constants as cst

#----------------------------------------------------------------------------------------

def print_status(p_m, cfp, cu, rcloneFilePath, ffm):
    error_occured = 0
    status_output = cst.STATUS
    status_output += f"\n\nOS : {cu.get_os()}"
    status_output += f"          Shell : {cu.shell_type()}"
    p_m_status = p_m.check_status(cu)
    status_output += f"{cst.P_MODE}{p_m_status}"
    cfp_status = cfp.check_status(cu)


    if ffm.is_file_present(rcloneFilePath) or ffm.is_file_present(rcloneFilePath+".exe") and ffm.is_file_present(rcloneFilePath+".1"):
        status_output += f"            {cst.RC_EXE}{cst.AVAILABLE}"
    else:
        status_output += f"            {cst.RC_EXE}{cst.MISSING}"
        error_occured += 1


    if p_m_status in (cst.ENABLED, cst.DISABLED):
        if p_m_status == cst.ENABLED:
            status_output += f"{cst.CF_PATH}{cfp_status}\n\n"
            if cfp_status != cst.AVAILABLE:
                    error_occured += 1
    else:
        error_occured += 1

    print(status_output)
    return error_occured

def take_input(p_m, cfp, cu):
    p_m.read_from_file()
    if p_mode_enabled(p_m, cu):
        cfp.read_from_file()
    
def p_mode_enabled(object, cu):
    return object.check_status(cu) == cst.ENABLED

        
#------------------------------------------------------------------------------------

def main():
    pm = PathManager()
    ffm = FileFolderManager()
    menu = Menu()
    cu = CommonUtils(pm)

    configPath = pm.join_rcstool_path(cst.CONFIG)
    rclonePath = pm.join_custom_path(configPath, cst.RCLONE_EXE_DIR)
    globalFilePath = pm.join_custom_path(configPath, cst.GLOBAL_FILE_TXT)
    confPath = pm.join_custom_path(configPath, cst.CONF)
    biwdPath = pm.join_custom_path(configPath, cst.BISYNC_WORKING_DIR)
    rcloneFilePath = pm.join_custom_path(rclonePath, cst.RCLONE_EXE_FILE)
    
    p_m = InputOutputFileOperations(cfg_path=globalFilePath, key=cst.P_MODE_KEY, prompt_message=cst.P_MODE_PROMPT)
    cfp = InputOutputFileOperations(cfg_path=globalFilePath, key=cst.CF_PATH_KEY, prompt_message=cst.CF_PATH_PROMPT.format(confPath), search_dir=confPath, search_extension=cst.CONF_EXTENSION,delimiter="->")

    isFirstRun = False
    choice = ""

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
        
    take_input(p_m, cfp, cu)
        
    while True:
        if choice.lower() != "e":
            cu.clear_screen()
            error_value = print_status(p_m, cfp, cu, rcloneFilePath, ffm)
            print(f"\n{cst.MAIN_MENU}")
            choice = input(f"\n{cst.TYPE_OPTION}")
            choice = choice.lower()

        if choice == "e":
            cu.clear_screen()
            print(f"{menu.print_header(cst.EGC_HEAD)}\n\n{cst.EGC_NOTE}")
            p_m.input_from_user()
            p_m.write_to_file()
            p_m.read_from_file()
            if p_mode_enabled(p_m, cu):
                if not ffm.is_dir_present(confPath):
                    ffm.create_dir(confPath)
                if not ffm.is_dir_present(biwdPath):
                    ffm.create_dir(biwdPath)
                cfp.user_selection_from_list()
                cfp.write_to_file()
                cfp.read_from_file()
            print("\n\nPress any key to return to the main menu...", end="")
            cu.pause()
            choice = ""
        elif choice == "r":
            take_input(p_m, cfp, cu)
        elif choice == "0":
            cu.clear_screen()
            break
        elif choice == "1":
            if error_value == 0:
                profilesync.main(pm, cu)
            else:
                cu.clear_screen()
                print("Global configuration is incomplete. Check Again...")
                time.sleep(3)
        else:
            cu.clear_screen()
            print("Invalid Option")
            time.sleep(3)
                

if __name__ == '__main__':
    main()
