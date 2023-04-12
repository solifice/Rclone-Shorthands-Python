import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if sys.platform.startswith('win'):
    # Windows implementation
    import msvcrt

    def get_char_input():
        return msvcrt.getch().decode()

elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    # Linux and macOS implementation
    import tty, termios

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def get_char_input():
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

else:
    # Unsupported platform
    def get_char_input():
        raise NotImplementedError("Sorry, your platform is not supported")
