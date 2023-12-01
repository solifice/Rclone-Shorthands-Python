import os
import sys
import rclone_shorthands_constants as cst
import psutil, re
import subprocess
import time
import threading
import keyboard

from rclone_shorthands_constants import CMDFlags

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
    def __init__(self, compatibility=None):
        self._compat_status = compatibility
        self._choose_operations()
        
    def _choose_operations(self):
        platform = sys.platform
        if platform.startswith('win'):
            self._python_exe = "python"
            self._which_os = cst.WINDOWS
            self._windows_operations()
        elif platform.startswith('linux'):
            self._python_exe = "python3"
            self._which_os = cst.LINUX
            self._posix_operations()
        elif platform.startswith('darwin'):
            self._python_exe = "python3"
            self._which_os = cst.MACOS
            self._posix_operations()
        else:
            self._which_os = "Other"
            self._other_operations()

    def _windows_operations(self):
        if self._compat_status.val == CMDFlags.PAUSE.val:
            self._pause_method = self._compat_pause
            is_posix = self._check_unix_shell()
            if not is_posix:
                is_windows = self._check_win_shell()
                if is_windows:
                    self._shell_type = "Windows Shell"
                    self._clear_screen = self._win_clrscr
                else:
                    self._shell_type = "Unknown Shell"
                    self._clear_screen = self._compat_clrscr
            else:
                self._shell_type = "Posix Shell"
                self._clear_screen = self._unix_clrscr
        elif self._compat_status.val == CMDFlags.CLEAR_SCREEN.val:
            self._clear_screen = self._compat_clrscr
            is_posix = self._check_unix_shell()
            if not is_posix:
                is_windows = self._check_win_shell()
                if is_windows:
                    self._shell_type = "Windows Shell"
                    self._pause_method = self._win_pause
                else:
                    self._shell_type = "Unknown Shell"
                    self._pause_method = self._compat_pause
            else:
                self._is_winpty = self._check_winpty()
                self._shell_type = "Posix Shell"
                if self._is_winpty or self._check_win_unix_term():
                    self._pause_method = self._win_pause
                else:
                    self._pause_method = self._compat_pause
        elif self._compat_status.val == CMDFlags.BOTH.val:
            self._pause_method = self._compat_pause
            self._clear_screen = self._compat_clrscr
            is_posix = self._check_unix_shell()
            if not is_posix:
                is_windows = self._check_win_shell()
                if is_windows:
                    self._shell_type = "Windows Shell"
                else:
                    self._shell_type = "Unknown Shell"
            else:
                self._is_winpty = self._check_winpty()
                self._shell_type = "Posix Shell"
        else:
            is_posix = self._check_unix_shell()
            if not is_posix:
                is_windows = self._check_win_shell()
                if is_windows:
                    self._shell_type = "Windows Shell"
                    self._clear_screen = self._win_clrscr
                    self._pause_method = self._win_pause
                else:
                    self._other_operations()
            else:
                self._shell_type = "Posix Shell"
                self._is_winpty = self._check_winpty()
                if self._is_winpty or self._check_win_unix_term():
                    self._pause_method = self._win_pause
                    self._clear_screen = self._unix_clrscr
                else:
                    self._clear_screen = self._unix_clrscr
                    self._pause_method = self._compat_pause
                    self._compat_status = "p"

    def _posix_operations(self):
        if self._compat_status.val == CMDFlags.PAUSE.val:
            self._pause_method = self._compat_pause
            if self._check_unix_shell():
                self._shell_type = "Posix Shell"
                self._clear_screen = self._unix_clrscr
            else:
                self._shell_type = "Unknown Shell"
                self._clear_screen = self._compat_clrscr
        elif self._compat_status.val == CMDFlags.CLEAR_SCREEN.val:
            self._clear_screen = self._compat_clrscr
            if self._check_unix_shell():
                self._shell_type = "Posix Shell"
                self._pause_method = self._posix_pause
            else:
                self._shell_type = "Unknown Shell"
                self._pause_method = self._compat_pause
        elif self._compat_status.val == CMDFlags.BOTH.val:
            self._pause_method = self._compat_pause
            self._clear_screen = self._compat_clrscr
            if self._check_unix_shell():
                self._shell_type = "Posix Shell"
            else:
                self._shell_type = "Unknown Shell"
        else:
            if self._check_unix_shell():
                self._shell_type = "Posix Shell"
                self._pause_method = self._posix_pause
                self._clear_screen = self._unix_clrscr
            else:
                self._other_operations()

    def _other_operations(self):
        self._compat_status = "cp"
        self._shell_type = "Unknown Shell"
        self._pause_method = self._compat_pause
        self._clear_screen = self._compat_clrscr
        
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
        input()
        
    def _unix_clrscr(self):
        return os.system("printf '\033c'")
        
    def _win_clrscr(self):
        return os.system("cls")
        
    def _compat_clrscr(self):
        import shutil
        return print("\n"*shutil.get_terminal_size().lines*2+'\033[1;1H', end='')

    def _check_unix_shell(self):
        try:
            exit_code = subprocess.run(['id'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False
                
    def _check_win_shell(self):
        current_process = psutil.Process()
        while current_process.parent() is not None:
            current_process = current_process.parent()
            parent_name = current_process.name()
            if re.fullmatch('pwsh|pwsh.exe|powershell|powershell.exe|cmd|cmd.exe', parent_name):
                return True
        return False
        
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
        
    def is_compat(self):
        return self._compat_status
        
    def get_py_exe(self):
        return self._python_exe