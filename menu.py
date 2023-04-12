import shutil

class Menu:
    def __init__(self):
        # Get terminal size using shutil
        self._terminal_width, _ = shutil.get_terminal_size()
        self._terminal_width = (int)(self._terminal_width/1.2)
        self._print_equal_to = f"{'=' * self._terminal_width}"
        self._print_hyphen = f"{'-' * self._terminal_width}"
        
    def print_equal_to(self):
        return self._print_equal_to

    def print_hyphen(self):
        return self._print_hyphen

    def print_header(self, prompt_message):
        return f"{self._print_equal_to}\n{prompt_message}\n{self._print_equal_to}"
