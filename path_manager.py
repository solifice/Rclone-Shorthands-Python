import os
import sys


class PathManager:
    def __init__(self):
        self._program_directory_path, self._is_executable_file = self._determine_program_directory_path()

    def _determine_program_directory_path(self):
        if getattr(sys, 'frozen', False):
            current_exe_file_path = os.path.abspath(sys.executable)
            return os.path.dirname(current_exe_file_path), True
        else:
            current_py_file_path = os.path.abspath(__file__)
            return os.path.dirname(current_py_file_path), False

    def get_program_directory_path(self):
        return self._program_directory_path

    def append_program_directory_path(self, file_or_directory_subpath):
        return os.path.join(self._program_directory_path, file_or_directory_subpath)

    @staticmethod
    def join_subpath(first_subpath, second_subpath):
        return os.path.join(first_subpath, second_subpath)

    def is_executable_file(self):
        return self._is_executable_file
