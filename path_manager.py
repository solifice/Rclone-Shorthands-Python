import os
import sys

class PathManager:
    def _get_current_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(os.path.abspath(sys.executable))
        else:
            return os.path.dirname(os.path.abspath(__file__))
            
    def create_path(self, relative_path, file_name):
        return os.path.join(self._get_current_path(), relative_path, file_name)