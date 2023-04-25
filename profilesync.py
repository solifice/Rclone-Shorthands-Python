import os
import time
from colorama import init, Fore, Style
from file_folder_manager import FileFolderManager
from menu import Menu
import common_utilities as cu
from input_output_file_operations import InputOutputFileOperations

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

def main(pm, cu):
    ffm = FileFolderManager()
    menu = Menu()
    choice = ""
    while choice != "x":
        syncProfile = "sync"
        sync_path = pm.join_rcstool_path(syncProfile)
        cu.clear_screen()
        profileSyncMenu = f"Profile Command: Sync"
        profileSyncMenu = menu.print_header(profileSyncMenu)
        profileSyncMenu += f"\n[X] | Return to Main Menu\n\n" \
                           f"[R] | Run Sync\n" \
                           f"[C] | Create Profile\n" \
                           f"[E] | Edit Profile\n" \
                           f"[D] | Delete Profile\n\n"

        print(profileSyncMenu)
        if not ffm.is_dir_present(sync_path):
            ffm.create_dir(sync_path)
        choice = input("Type Option: ")
        choice = choice.lower()
        if choice == "x":
            return
        elif choice == "c":
            profileName = ""
            while not profileName.strip():
                cu.clear_screen()
                invalid_names = ['CON', 'PRN', 'AUX', 'NUL']
                invalid_names += ['COM{}'.format(i) for i in range(1, 10)]
                invalid_names += ['LPT{}'.format(i) for i in range(1, 10)]
                
                profileName = input("Profile Name: ")
                
                if not any(char in profileName for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']) and not profileName.upper() in invalid_names:
                
                    profilePath = pm.join_custom_path(sync_path, profileName + ".ini")
                    if ffm.is_file_present(profilePath):
                        cu.clear_screen()
                        print("Profile with this name already exists, please try other names...")
                        print("Returning back...")
                        time.sleep(1)
                    else:
                        if not ffm.is_file_present(profilePath):
                            ffm.create_file(profilePath)
                        cu.clear_screen()
                        print("Successfully Created Profile")
                        time.sleep(1)
                        cu.clear_screen()
                        source = InputOutputFileOperations(cfg_path=profilePath, key='source', prompt_message='Enter your source path-> ', delimiter='->')
                        source.input_from_user()
                        source.write_to_file()
                        time.sleep(1)
                        destn = InputOutputFileOperations(cfg_path=profilePath, key='destination', prompt_message='\n\nEnter your destination path->', delimiter='-> ')
                        destn.input_from_user()
                        destn.write_to_file()
                        time.sleep(1)
                        inct = InputOutputFileOperations(cfg_path=profilePath, key='interactive', prompt_message='\n\nDo you want interactive method (Y/N)= ')
                        inct.input_from_user()
                        inct.write_to_file()
                        time.sleep(1)
                        dry_run = InputOutputFileOperations(cfg_path=profilePath, key='dry_run', prompt_message='\n\nDo you want to dry run before proceeding (Y/N)= ')
                        dry_run.input_from_user()
                        dry_run.write_to_file()
                        time.sleep(1)
                else:
                    cu.clear_screen()
                    print("Invalid profile name..")
                    print("Try Again..")
                    time.sleep(1)

        elif choice == "r":
            cu.clear_screen()
            p_p = InputOutputFileOperations(prompt_message=f"\n\nSelect any preset from below:- ({Fore.LIGHTCYAN_EX}{sync_path}{Style.RESET_ALL})\n", search_dir=sync_path, search_extension=".ini")
            p_p.user_selection_from_list()