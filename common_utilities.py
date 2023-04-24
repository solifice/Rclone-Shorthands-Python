import os
import sys
import rclone_shorthands_constants as cst
import psutil, re
import subprocess
import time

class CommonUtils:
    def __init__(self, pm):
        self._choose_operations(pm)
        
    def _choose_operations(self, pm):
        platform = sys.platform
        if platform.startswith('win'):
            self._which_os, self.shell_type, self._clear_screen, self._pause_method = self._windows_operations(pm)
            print(self.shell_type)
        elif platform.startswith('linux'):
            self._which_os, self._clear_screen, self._pause_method = self._linux_operations()
        elif platform.startswith('darwin'):
            self._which_os, self._clear_screen, self._pause_method = self._mac_operations()
        else:
            self._which_os, self._clear_screen, self._pause_method = self._other_operations()
            
    def _windows_operations(self, pm):
        import msvcrt
        is_unix_shell= self._check_unix_shell() =="Not Unix"
        if is_unix_shell:
            return cst.WINDOWS, self._check_win_shell(), lambda: os.system("cls"), lambda: msvcrt.getch()
        else:
            print("this")
            return cst.WINDOWS, is_unix_shell, lambda: os.system('printf "\033c"'), input
                 
    def _linux_operations(self):
        clear_screen, pause_method = self._linux_mac_common()
        return cst.LINUX, clear_screen, pause_method
        
    def _mac_operations(self):
        clear_screen, pause_method = self._linux_mac_common()
        return cst.MACOS, clear_screen, pause_method
        
    def _other_operations(self):
        import shutil
        return "Other", lambda: print(shutil.get_terminal_size().lines*2+'\033[1;1H', end=''), input
    
    def _linux_mac_common(self):
        import termios
        import tty
        def _getch():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
        return lambda: os.system("printf '\033c'"), _getch

    def _check_unix_shell(self):
        try: 
            shell_name = os.path.basename(os.environ["SHELL"]).lower()
            for element in cst.SHELLS:
                if element in shell_name:
                    return cst.SHELLS[element]
            return 'Other Unix Shell'
        except KeyError:
            try:
                exit_code = subprocess.run(['id'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return 'Other Unix Shell'
            except FileNotFoundError:
                return 'Not Unix'
                
    def _check_win_shell(self):
        pproc_name = psutil.Process(os.getppid()).name()
        is_power_shell = bool(re.fullmatch('pwsh|pwsh.exe|powershell.exe', pproc_name))
        if is_power_shell:
            return 'Powershell'
        return 'Command Prompt'

    def get_os(self):
        return self._which_os
    
    def pause(self):
        return self._pause_method()
        
    def clear_screen(self):
        return self._clear_screen()
    
    def shell_type(self):
        return self.shell_type
