import setglobalconfigs
from colorama import init, Fore, Style

def main():
    setglobalconfigs.clearScreen()
    profileSyncMenu = (f"{setglobalconfigs.separator('=')}\n"
                f"Profile Command: Sync\n"
                f"{setglobalconfigs.separator('=')}\n\n"
                f"[X] | Return to Main Menu\n\n"
                f"[R] | Run Sync\n"
                f"[C] | Create Profile\n"
                f"[E] | Edit Profile\n"
                f"[D] | Delete Profile\n\n")
    print(profileSyncMenu)
    
    input("Type Option: ")