import os

class PathManager:
    def _get_current_path():
        if getattr(sys, 'frozen', False):
            return os.path.dirname(os.path.abspath(sys.executable))
        else:
            return os.path.dirname(os.path.abspath(__file__))
            
    def create_path(relative_path, file_name):
        return os.path.join(_get_current_path(), relative_path, file_name)