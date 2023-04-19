import os
import sys
import rclone_shorthands_constants as cst

class CommonUtils:
    def __init__(self):
        self._choose_operations()
        
    def _choose_operations(self):
        platform = sys.platform
        if platform.startswith('win'):
            self._which_os, self._clear_screen, self._pause_method = self._windows_operations()
        elif platform.startswith('linux'):
            self._which_os, self._clear_screen, self._pause_method = self._linux_operations()
        elif platform.startswith('darwin'):
            self._which_os, self._clear_screen, self._pause_method = self._mac_operations()
        else:
            self._which_os, self._clear_screen, self._pause_method = self._other_operations()
            
    def _windows_operations(self):
        import msvcrt
        return cst.WINDOWS, lambda: os.system("cls"), lambda: msvcrt.getch().decode()
        
    def _linux_operations(self):
        clear_screen, pause_method = self._linux_mac_common()
        return cst.LINUX, clear_screen, pause_method
        
    def _mac_operations(self):
        clear_screen, pause_method = self._linux_mac_common()
        return cst.MACOS, clear_screen, pause_method
        
    def _other_operations(self):
        import shutil
        return "Other", lambda: print(shutil.get_terminal_size().lines, end=''), input
    
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

    def get_os(self):
        return self._which_os
    
    def pause(self):
        return self._pause_method()
        
    def clear_screen(self):
        return self._clear_screen()
    