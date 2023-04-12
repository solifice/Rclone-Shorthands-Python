import os
import sys

class PathManager:
    def __init__(self):
        self._current_path = self._enumerate_current_path()
        
    def _enumerate_current_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(os.path.abspath(sys.executable))
        else:
            return os.path.dirname(os.path.abspath(__file__))
            
    def get_rcstool_path(self):
        return self._current_path
        
    def join_rcstool_path(self, file_dir_name):
        return os.path.join(self._current_path, file_dir_name)
        
    def join_custom_path(self, custom_path, file_dir_name):
        return os.path.join(custom_path, file_dir_name)