import dill
import base64
import subprocess
import argparse

import file_folder_manager as ffm

from path_manager import PathManager
from common_utilities import CommonUtils
from rclone_shorthands_constants import CMDFlags, ModuleLauncher


def main():
    path_manager = PathManager()
    common_utils = CommonUtils()
    if path_manager.is_executable_file():
        select_path_to_main_application = path_manager.append_program_directory_path(
            ModuleLauncher.FILE_MENU_SETTINGS_HANDLER.value)
        if ffm.is_file_present(select_path_to_main_application):
            command = [select_path_to_main_application]
        else:
            print("setglobalconfigs.file is missing, reinstall the program")
            del path_manager
            exit(0)
    elif common_utils.check_python_version():
        select_path_to_main_application = path_manager.append_program_directory_path(
            ModuleLauncher.PY_MENU_SETTINGS_HANDLER.value)
        if ffm.is_file_present(select_path_to_main_application):
            command = [common_utils.generate_python_string(
            ), select_path_to_main_application]
        else:
            print("setglobalconfigs.py is missing, reinstall the program")
            del path_manager
            exit(0)
    else:
        print("Python version 3 or above required")
        del path_manager
        exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--console", help="Specify the type of console to use. Options: cls, pause, both",
                        choices=[flag.arg for flag in CMDFlags], default=None)
    args = parser.parse_args()

    if common_utils.check_winpty():
        command.insert(0, "winpty")
        common_utils.clear_screen()

    encoded_path_manager = base64.b64encode(
        dill.dumps(path_manager)).decode('utf-8')

    result = None

    while True:
        new_command = command[:]
        list_returncodes = {flag.returncode: flag for flag in CMDFlags}
        if result != None:
            if result.returncode in list_returncodes:
                common_utils.continue_operations(
                    list_returncodes.get(result.returncode))
            else:
                break
        else:
            arguments_to_value = {flag.arg: flag for flag in CMDFlags}
            if args.console is not None:
                common_utils.continue_operations(
                    arguments_to_value.get(args.console))
            else:
                common_utils.continue_operations(CMDFlags.COMPAT_OFF)

        encoded_common_utils = base64.b64encode(
            dill.dumps(common_utils)).decode('utf-8')

        new_command.extend(["-i", encoded_path_manager, encoded_common_utils])

        del common_utils
        result = subprocess.run(new_command)
        del new_command
        del encoded_common_utils
    del path_manager
    del new_command
    del result
    del args
    exit(0)


if __name__ == '__main__':
    main()
