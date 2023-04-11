from path_manager import PathManager
import os
import time
from colorama import init, Fore, Style
from file_folder_manager import FileFolderManager
from menu import Menu
import common_utilities as cu

def listProfiles(parent_folder, profile_name):
    profile_folders = []
    for folder in os.listdir(parent_folder):
        if os.path.isdir(os.path.join(parent_folder, folder)):
            if "profile.txt" in os.listdir(os.path.join(parent_folder, folder)):
                profile_folders.append(folder)

    print("Profile Folders:")
    for i, folder in enumerate(profile_folders):
        print(f"[{i+1}] {folder}")
        
    selected_folder = input("Enter the number of the profile folder you want to select: ")
    if selected_folder.isdigit() and int(selected_folder) <= len(profile_folders):
        selected_folder_name = profile_folders[int(selected_folder)-1]
        print(f"You have selected {selected_folder_name}")
    else:
        print("Invalid selection.")

def main():
    pm = PathManager()
    ffm = FileFolderManager()
    menu = Menu()
    choice = ""
    while choice != "x":
        syncProfile = "sync"
        syncProfilePath = pm.create_path(syncProfile, "")
        cu.clear_screen()
        profileSyncMenu = f"Profile Command: Sync"
        profileSyncMenu = menu.print_header(profileSyncMenu)
        profileSyncMenu += f"\n[X] | Return to Main Menu\n\n" \
                           f"[R] | Run Sync\n" \
                           f"[C] | Create Profile\n" \
                           f"[E] | Edit Profile\n" \
                           f"[D] | Delete Profile\n\n"

        print(profileSyncMenu)
        if not ffm.is_dir_present(syncProfilePath):
            ffm.create_dir(syncProfilePath)
        choice = input("Type Option: ")
        choice = choice.lower()
        if choice == "x":
            return
        elif choice == "c":
            profileName = ""
            while not profileName.strip():
                cu.clear_screen()
                profileName = input("Profile Name: ")
            profilePath = pm.create_path(syncProfile, profileName)
            profileTxtPath = pm.create_path(profilePath, "syncProfile.txt")
            if ffm.is_dir_present(profilePath) and ffm.is_file_present(profileTxtPath):
                cu.clear_screen()
                print("Profile with this name already exists, please try other names...")
                print("Returning back...")
                time.sleep(3)
            else:
                if not ffm.is_dir_present(profilePath):
                    ffm.create_dir(profilePath)
                if not ffm.is_file_present(profileTxtPath):
                    ffm.create_file(profileTxtPath)
                cu.clear_screen()
                print("Successfully Created Profile")
                time.sleep(3)