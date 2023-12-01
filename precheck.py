import dill
import base64
import subprocess
import argparse
import sys

import file_folder_manager as ffm

from path_manager import PathManager
from common_utilities import CommonUtils
from rclone_shorthands_constants import CMDFlags


def main():
    path_manager = PathManager()
    if not path_manager.is_executable_file():
        if sys.version_info < (3, 0):
            print("Python version 3 supported...")
            del path_manager
            exit(0)

    path_to_main_application_file = path_manager.append_program_directory_path(
        "setglobalconfigs.file")
    path_to_main_application_py = path_manager.append_program_directory_path(
        "setglobalconfigs.py")

    if ffm.is_file_present(path_to_main_application_file):
        select_path_to_main_application = [f"{path_to_main_application_file}"]
        is_application_program_py = False
    elif ffm.is_file_present(path_to_main_application_py):
        select_path_to_main_application = [path_to_main_application_py]
        is_application_program_py = True
    else:
        print("setglobalconfigs is missing, reinstall the program")
        del path_manager
        exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--console", help="Specify the type of console to use. Options: cls, hold, both",
                        choices=[flag.arg for flag in CMDFlags], default=None)
    args = parser.parse_args()

    encoded_path_manager = base64.b64encode(
        dill.dumps(path_manager)).decode('utf-8')

    result = None

    while True:
        command = select_path_to_main_application[:]
        list_returncodes = {flag.returncode: flag for flag in CMDFlags}
        if result != None:
            if result.returncode in list_returncodes:
                common_utils = CommonUtils(
                    list_returncodes.get(result.returncode))
            else:
                break
        else:
            arguments_to_value = {flag.arg: flag for flag in CMDFlags}
            if args.console is not None:
                common_utils = CommonUtils(
                    arguments_to_value.get(args.console))
            else:
                common_utils = CommonUtils(CMDFlags.COMPAT_OFF)

        encoded_common_utils = base64.b64encode(
            dill.dumps(common_utils)).decode('utf-8')

        if is_application_program_py:
            command.insert(0, common_utils.get_py_exe())

        if common_utils.check_winpty():
            command.insert(0, "winpty")
            common_utils.clear_screen()

        command.extend(["-i", encoded_path_manager, encoded_common_utils])

        del common_utils
        result = subprocess.run(command)
        del command
        del encoded_common_utils
    del path_manager
    del command
    del result
    del args
    del is_application_program_py
    exit(0)


if __name__ == '__main__':
    main()
