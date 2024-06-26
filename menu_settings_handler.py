from status_io_manager import StatusIOManager
import os
import time
import profilesync
import file_folder_manager as ffm
from menu import Menu
from path_manager import PathManager
from common_utilities import CommonUtils
import rclone_shorthands_constants as cst
import argparse
import dill
import base64

from rclone_shorthands_constants import Status
from rclone_shorthands_constants import DataType

# ----------------------------------------------------------------------------------------


def print_status(p_m, cfp, cu, rcloneFilePath, ffm):
    error_occured = 0
    status_output = cst.STATUS
    status_output += f"\n\nOS: {cu.get_os()}"
    status_output += f"          Shell: {cu.shell_type()}"

    if ffm.is_file_present(rcloneFilePath) or ffm.is_file_present(rcloneFilePath+".exe") and ffm.is_file_present(rcloneFilePath+".1"):
        status_output += f"            {cst.RC_EXE}{Status.AVAILABLE_FILE.prt}"
    else:
        status_output += f"            {cst.RC_EXE}{Status.MISSING.prt}"
        error_occured += 1

    p_m_status = p_m.check_status(cu)
    status_output += f"{cst.P_MODE}{p_m_status.prt}"
    cfp_status = cfp.check_status(cu)

    if p_m_status.val in (Status.ENABLED.val, Status.DISABLED.val):
        if p_m_status.val == Status.ENABLED.val:
            if cfp_status.val == Status.AVAILABLE_DIRECTORY.val:
                status_output += f"{cst.CF_PATH}{Status.NOT_EXISTS.prt}\n\n"
            else:
                status_output += f"{cst.CF_PATH}{cfp_status.prt}\n\n"
            if cfp_status.val != Status.AVAILABLE_FILE.val:
                error_occured += 1
            if cfp_status.val == Status.AVAILABLE_FILE.val:
                os.environ["RCLONE_CONFIG_PATH"] = "--config=" + cfp.value
    else:
        error_occured += 1

    print(status_output)
    return error_occured


def take_input(p_m, cfp, cu):
    p_m.read_from_file()
    if p_mode_enabled(p_m, cu):
        cfp.read_from_file()


def p_mode_enabled(object, cu):
    return object.check_status(cu).val == Status.ENABLED.val


# ------------------------------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", nargs=2, required=True)
    parser.add_argument("-c", action="store_true")
    args = parser.parse_args()

    path_manager = dill.loads(base64.b64decode(args.i[0].encode('utf-8')))
    cu = dill.loads(base64.b64decode(args.i[1].encode('utf-8')))

    menu = Menu()

    configPath = path_manager.append_program_directory_path(cst.CONFIG)
    rclonePath = path_manager.join_subpath(configPath, cst.RCLONE_EXE_DIR)
    globalFilePath = path_manager.join_subpath(configPath, cst.GLOBAL_FILE_TXT)
    confPath = path_manager.join_subpath(configPath, cst.CONF)
    biwdPath = path_manager.join_subpath(configPath, cst.BISYNC_WORKING_DIR)
    rcloneFilePath = path_manager.join_subpath(rclonePath, cst.RCLONE_EXE_FILE)

    p_m = StatusIOManager(
        file_path=globalFilePath, key=cst.P_MODE_KEY, prompt_message=cst.P_MODE_PROMPT, value_type=DataType.YESNO)
    cfp = StatusIOManager(file_path=globalFilePath, key=cst.CF_PATH_KEY, prompt_message=cst.CF_PATH_PROMPT,
                          search_directory=confPath, search_extension=cst.CONF_EXTENSION, value_type=DataType.LOCAL_PATH)

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
    path_to_add = rclonePath
    os.environ["PATH"] += os.pathsep + path_to_add

    while True:
        if choice != "e":
            cu.clear_screen()
            error_value = print_status(p_m, cfp, cu, rcloneFilePath, ffm)
            # print(f"\n{cst.MAIN_MENU.format(cu.is_compat().prt)}")
            choice = input(f"\n{cst.TYPE_OPTION}").strip().lower()

        if choice == "e":
            cu.clear_screen()
            print(f"{menu.print_header(cst.EGC_HEAD)}\n\n{cst.EGC_NOTE}")
            p_m.get_user_input_from_console()
            p_m.write_to_file()
            p_m.read_from_file()
            if p_mode_enabled(p_m, cu):
                if not ffm.is_dir_present(confPath):
                    ffm.create_dir(confPath)
                if not ffm.is_dir_present(biwdPath):
                    ffm.create_dir(biwdPath)
                cfp.get_user_choice_from_console()
                cfp.write_to_file()
                cfp.read_from_file()
            print("\n\nPress any key to return to the main menu...", end="")
            cu.pause()
            choice = ""
        elif choice == "c":
            cu.clear_screen()
            print(
                "1 - Start Clearscreen\n2 - Start Pause\n3 - Start Both\n4 - Start Normal\nEnter - To return")
            c = input("Type Options: ")
            if c.strip().lower() == "1":
                exit(5)
            elif c.strip().lower() == "2":
                exit(6)
            elif c.strip().lower() == "3":
                exit(7)
            elif c.strip().lower() == "4":
                exit(8)
            else:
                pass
        elif choice == "r":
            take_input(p_m, cfp, cu)
        elif choice == "0":
            cu.clear_screen()
            break
        elif choice == "1":
            if error_value == 0:
                profilesync.main(path_manager, cu)
            else:
                cu.clear_screen()
                print("Global configuration is incomplete. Check Again...")
                time.sleep(3)
        else:
            cu.clear_screen()
            print("Invalid Option")
            time.sleep(3)


if __name__ == '__main__':

    filename, file_extension = os.path.splitext(__file__)
    if file_extension not in (".py", ".file"):
        print("This script can only be executed without file extension.")
        exit()

    main()
