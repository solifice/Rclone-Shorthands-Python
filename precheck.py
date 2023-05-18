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
    pm = PathManager()
    if not pm.is_exe():
        if sys.version_info < (3, 0):
            print("Python version 3 supported...")
            del pm
            exit(0)
            
    if ffm.is_file_present(pm.join_rcstool_path("setglobalconfigs.file")):
        command = [f"{pm.join_rcstool_path('setglobalconfigs.file')}"]
        check = 0
    elif ffm.is_file_present(pm.join_rcstool_path("setglobalconfigs.py")):
        command = [pm.join_rcstool_path('setglobalconfigs.py')]
        check = 1
    else:
        print("setglobalconfigs is missing, reinstall the program")
        del pm
        exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--console", help="Specify the type of console to use. Options: cls, hold, both", choices=[flag.arg for flag in CMDFlags], default=None)
    args = parser.parse_args()
    
    opm = base64.b64encode(dill.dumps(pm)).decode('utf-8')
    
    result = None
    
    while True:
        cmd = command[:]
        abc = {flag.returncode: flag for flag in CMDFlags}
        if result != None:
            if result.returncode in abc:
                cu = CommonUtils(abc.get(result.returncode))
            else:
                break
        else:
            arg_to_val = {flag.arg: flag for flag in CMDFlags}
            if args.console is not None:
                cu = CommonUtils(arg_to_val.get(args.console))
            else:
                cu = CommonUtils(CMDFlags.COMPAT_OFF)
    
        ocu = base64.b64encode(dill.dumps(cu)).decode('utf-8')
    
        if check:
            cmd.insert(0, cu.get_py_exe())
        
        if cu.check_winpty():
            cmd.insert(0, "winpty")
            cu.clear_screen()
            
        cmd.extend(["-i", opm, ocu])
                
        del cu
        result = subprocess.run(cmd)
        del cmd
        del ocu
    del pm
    del command
    del result
    del args
    del check
    exit(0)

if __name__ == '__main__':
    main()