import os
import sys

class PathManager:
    def __init__(self):
        self._current_path, self._script_name, self._is_exe = self._enumerate_current_path()
        
    def _enumerate_current_path(self):
        if getattr(sys, 'frozen', False):
            abs_path = os.path.abspath(sys.executable)
            return os.path.dirname(abs_path), os.path.basename(abs_path), True
        else:
            abs_path = os.path.abspath(__file__)
            return os.path.dirname(abs_path), "test2.py", False
            
    def get_rcstool_path(self):
        return self._current_path
        
    def join_rcstool_path(self, file_dir_name):
        return os.path.join(self._current_path, file_dir_name)
        
    def join_custom_path(self, custom_path, file_dir_name):
        return os.path.join(custom_path, file_dir_name)
        
    def is_exe(self):
        return self._is_exe
        
    def get_script_name(self):
        return self._script_name