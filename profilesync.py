from path_manager import PathManager
import setglobalconfigs
import globalfunctions
import os
import time
from colorama import init, Fore, Style

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
    choice = ""
    while choice != "x":
        syncProfile = "sync"
        syncProfilePath = pm.create_path(syncProfile, "")
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
        if not globalfunctions.isDirPresent(syncProfilePath):
            globalfunctions.createDir(syncProfilePath)
        choice = input("Type Option: ")
        choice = choice.lower()
        if choice == "x":
            return
        elif choice == "c":
            profileName = ""
            while not profileName.strip():
                setglobalconfigs.clearScreen()
                profileName = input("Profile Name: ")
            profilePath = globalfunctions.createPath(syncProfile, profileName)
            profileTxtPath = globalfunctions.createPath(profilePath, "syncProfile.txt")
            if globalfunctions.isDirPresent(profilePath) and globalfunctions.isFilePresent(profileTxtPath):
                setglobalconfigs.clearScreen()
                print("Profile with this name already exists, please try other names...")
                print("Returning back...")
                time.sleep(3)
            else:
                if not globalfunctions.isDirPresent(profilePath):
                    globalfunctions.createDir(profilePath)
                if not globalfunctions.isFilePresent(profileTxtPath):
                    globalfunctions.createFile(profileTxtPath)
                setglobalconfigs.clearScreen()
                print("Successfully Created Profile")
                time.sleep(3)