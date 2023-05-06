import dill
import base64
import subprocess
import argparse
import sys

import file_folder_manager as ffm
from path_manager import PathManager
from common_utilities import CommonUtils

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
    parser.add_argument("-c", "--console", help="Specify the type of console to use. Options: cls, hold, both", choices=["cls", "hold", "both"], default=None)
    args = parser.parse_args()
    
    opm = base64.b64encode(dill.dumps(pm)).decode('utf-8')
    
    result = None
    
    while True:
        cmd = command[:]
        if result != None:
            if result.returncode == 5:
                cu = CommonUtils("c")
            elif result.returncode == 6:
                cu = CommonUtils("p")
            elif result.returncode == 7:
                cu = CommonUtils("pc")
            elif result.returncode == 8:
                cu = CommonUtils()
            else:
                break
        else:
            if args.console is not None:
                if args.console == "cls":
                    cu = CommonUtils("c")
                elif args.console == "hold":
                    cu = CommonUtils("p")
                elif args.console == "both":
                    cu = CommonUtils("pc")
            else:
                cu = CommonUtils()
    
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