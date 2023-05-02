import dill
import base64
import sys
import subprocess
import argparse

import file_folder_manager as ffm
from path_manager import PathManager
from common_utilities import CommonUtils

def main(): 

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--console", help="Specify the type of console to use. Options: cls, hold, both", choices=["cls", "hold", "both"], default=None)
    args = parser.parse_args()
    
    if args.console is not None:
        if args.console == "cls":
            cu = CommonUtils("c")
        elif args.console == "hold":
            cu = CommonUtils("p")
        elif args.console == "both":
            cu = CommonUtils("pc")
    else:
        cu = CommonUtils()
        
    pm = PathManager()
    
    opm = base64.b64encode(dill.dumps(pm)).decode('utf-8')
    ocu = base64.b64encode(dill.dumps(cu)).decode('utf-8')
    
    if ffm.is_file_present(pm.join_rcstool_path("setglobalconfigs.file")):
        cmd = [f"{pm.join_rcstool_path('setglobalconfigs.file')}"]
    elif ffm.is_file_present(pm.join_rcstool_path("setglobalconfigs.py")):
        cmd = ["python", pm.join_rcstool_path('setglobalconfigs.py')]
    else:
        print("setglobalconfigs is missing, reinstall the program")
        sys.exit()
    
    if cu.check_winpty():
        cmd.insert(0, "winpty")
        cu.clear_screen()
        
    cmd.extend(["-i", opm, ocu])
            
    del pm
    del cu
    subprocess.run(cmd)
    sys.exit()

if __name__ == '__main__':
    main()