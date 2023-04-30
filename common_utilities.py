import os
import sys
import rclone_shorthands_constants as cst
import psutil, re
import subprocess
import time
import threading
import keyboard

lock = threading.Lock()

class TimeoutException(Exception):
    pass
    
def auto_type():
    with lock:
        time.sleep(0.7)
        keyboard.press(" ")
        keyboard.release(" ")
        
def timeout_handler():
    print("\nIt looks like the current terminal isn't compatible with some functions of the program, Try with some other terminal emulator or run the program with arguments like ./program.exe -c to run in the same terminal\nExiting Now...", flush = True)
    os._exit(1)

class CommonUtils:
    def __init__(self):
        self._choose_operations()
        
    def _choose_operations(self):
        platform = sys.platform
        if platform.startswith('win'):
            self._which_os, self._shell_type, self._clear_screen, self._pause_method = self._windows_operations()
        elif platform.startswith('linux'):
            self._which_os, self._shell_type, self._clear_screen, self._pause_method = self._linux_operations()
        elif platform.startswith('darwin'):
            self._which_os, self._shell_type, self._clear_screen, self._pause_method = self._mac_operations()
        else:
            self._which_os, self._shell_type, self._clear_screen, self._pause_method = self._other_operations()
            
    def _windows_operations(self):
        shell_name = self._check_unix_shell()
        if shell_name == "Not Unix":
            shell_name = self._check_win_shell()
            if shell_name in ("Powershell", "Command Prompt"):
                return cst.WINDOWS, shell_name, self._win_clrscr, self._win_pause
            else:
                return cst.WINDOWS, shell_name, self._compat_clrscr, self._compat_pause
        else:
            self._is_winpty = self._check_winpty()
            if self._is_winpty:
                return cst.WINDOWS, shell_name, self._unix_clrscr, self._win_pause
            elif self._check_win_unix_term():
                return cst.WINDOWS, shell_name, self._unix_clrscr, self._win_pause
            else:
                return cst.WINDOWS, shell_name, self._unix_clrscr, self._compat_pause
        
    def _linux_operations(self):
        shell_name = self._check_unix_shell()
        if shell_name == "Not Unix":
            return cst.LINUX, shell_name, self._compat_clrscr, self._compat_pause
        return cst.LINUX, shell_name, self._unix_clrscr, self._posix_pause
        
    def _mac_operations(self):
        shell_name = self._check_unix_shell()
        if shell_name == "Not Unix":
            return cst.MACOS, shell_name, self._compat_clrscr, self._compat_pause
        return cst.MACOS, self._check_unix_shell(), self._unix_clrscr, self._posix_pause
        
    def _other_operations(self):
        return "Other", "Other", self._unix_clrscr, self._compat_pause
        
    def _posix_pause(self):
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
            
    def _win_pause(self):
        import msvcrt
        return msvcrt.getch()
        
    def _compat_pause(self):
        import getpass
        getpass.getpass()
        
    def _unix_clrscr(self):
        return os.system("printf '\033c'")
        
    def _win_clrscr(self):
        return os.system("cls")
        
    def _compat_clrscr():
        import shutil
        return print("\n"*shutil.get_terminal_size().lines*2+'\033[1;1H', end='')
        
    def _check_unix_shell(self):
        try: 
            detected_shell = os.path.basename(os.environ["SHELL"]).lower()
            for each_shell in cst.SHELLS:
                if each_shell in detected_shell:
                    return cst.SHELLS[each_shell]
            return 'Other Unix Shell'
        except KeyError:
            try:
                exit_code = subprocess.run(['id'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return 'Other Unix Shell'
            except FileNotFoundError:
                return 'Not Unix'
                
    def _check_win_shell(self):
        current_process = psutil.Process()
        while current_process.parent() is not None:
            current_process = current_process.parent()
            parent_name = current_process.name()
            if re.fullmatch('pwsh|pwsh.exe|powershell.exe', parent_name):
                return "Powershell"
            if re.fullmatch('cmd|cmd.exe', parent_name):
                return "Command Prompt"
        return "Other"
        
    def _check_winpty(self):
        try:
            subprocess.run(['winpty', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except:     
            return False
        
    def _check_win_unix_term(self):
        print("Analysing terminal support...", end='', flush=True)
        auto_type_thread = threading.Thread(target=auto_type)
        try:
            timer = threading.Timer(1.5, timeout_handler)
            timer.start()
            auto_type_thread.start()
            import msvcrt
            msvcrt.getch()
        except Exception as e:
            print("Error Occured")
            return False
        finally:
            auto_type_thread.join()
            timer.cancel()
            timer.join()
        print("\nDone")
        return True
       
    @staticmethod
    def check_argument(arg):
        return arg in sys.argv

    def get_os(self):
        return self._which_os
    
    def pause(self):
        return self._pause_method()
        
    def clear_screen(self):
        return self._clear_screen()
    
    def shell_type(self):
        return self._shell_type
        
    def check_winpty(self):
        return getattr(self, '_is_winpty', False) is True