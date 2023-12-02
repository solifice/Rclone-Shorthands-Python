import os
import time
from colorama import init, Fore, Style
import file_folder_manager as ffm
from menu import Menu
from input_output_file_operations import InputOutputFileOperations
import subprocess

from rclone_shorthands_constants import Status
from rclone_shorthands_constants import DataType
import logging

logging.basicConfig(
    # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('example.log'),  # Save logs to a file
        logging.StreamHandler()           # Print logs to the console
    ]
)


def listProfiles(parent_folder, profile_name):
    profile_folders = []
    for folder in os.listdir(parent_folder):
        if os.path.isdir(os.path.join(parent_folder, folder)):
            if "profile.txt" in os.listdir(os.path.join(parent_folder, folder)):
                profile_folders.append(folder)

    print("Profile Folders:")
    for i, folder in enumerate(profile_folders):
        print(f"[{i+1}] {folder}")

    selected_folder = input(
        "Enter the number of the profile folder you want to select: ")
    if selected_folder.isdigit() and int(selected_folder) <= len(profile_folders):
        selected_folder_name = profile_folders[int(selected_folder)-1]
        print(f"You have selected {selected_folder_name}")
    else:
        print("Invalid selection.")


def main(path_manager, cu):
    menu = Menu()
    choice = ""
    while choice != "x":
        syncProfile = "sync"
        sync_path = path_manager.append_program_directory_path(syncProfile)
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
        choice = input("Type Option: ").strip().lower()
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

                    profilePath = path_manager.join_subpath(
                        sync_path, profileName + ".ini")
                    if ffm.is_file_present(profilePath):
                        cu.clear_screen()
                        print(
                            "Profile with this name already exists, please try other names...")
                        print("Returning back...")
                        time.sleep(1)
                    else:
                        if not ffm.is_file_present(profilePath):
                            ffm.create_file(profilePath)
                        cu.clear_screen()
                        print("Successfully Created Profile")
                        time.sleep(1)
                        cu.clear_screen()
                        source = InputOutputFileOperations(
                            file_path=profilePath, key='source', prompt_message='Enter your source path-> ', value_type=DataType.PATH)
                        source.get_user_input_from_console()
                        source.write_to_file()
                        time.sleep(1)
                        destn = InputOutputFileOperations(
                            file_path=profilePath, key='destination', prompt_message='\n\nEnter your destination path->', value_type=DataType.PATH)
                        destn.get_user_input_from_console()
                        destn.write_to_file()
                        time.sleep(1)
                        inct = InputOutputFileOperations(
                            file_path=profilePath, key='interactive', prompt_message='\n\nDo you want interactive method (Y/N)= ', value_type=DataType.YESNO)
                        inct.get_user_input_from_console()
                        inct.write_to_file()
                        time.sleep(1)
                        dry_run = InputOutputFileOperations(
                            file_path=profilePath, key='dry_run', prompt_message='\n\nDo you want to dry run before proceeding (Y/N)= ', value_type=DataType.YESNO)
                        dry_run.get_user_input_from_console()
                        dry_run.write_to_file()
                        time.sleep(1)
                        cu.clear_screen()
                        print("Profile updated with configurations")
                        time.sleep(1)
                else:
                    cu.clear_screen()
                    print("Invalid profile name..")
                    print("Try Again..")
                    time.sleep(1)

        elif choice == "r":
            cu.clear_screen()
            message = ("Select a preset :- ", f"No presets were found, copy-paste your preset ini file to {{}} and press R to refresh, press any other key to go back...", "going back...",
                       f"Presets were found, Select your desired preset, You can copy-paste your preset ini file to {{}} and press R to refresh, your new preset will be visible", "No selection was made, going back...")
            p_p = InputOutputFileOperations(
                prompt_message=message, search_directory=sync_path, search_extension=".ini")
            p_p.get_user_choice_from_console()
            if p_p.value is not None:
                source = InputOutputFileOperations(
                    file_path=p_p.value, key='source', value_type=DataType.PATH)
                source.read_from_file()
                destn = InputOutputFileOperations(
                    file_path=p_p.value, key='destination', value_type=DataType.PATH)
                destn.read_from_file()
                inct = InputOutputFileOperations(
                    file_path=p_p.value, key='interactive', value_type=DataType.YESNO)
                inct.read_from_file()
                dry_run = InputOutputFileOperations(
                    file_path=p_p.value, key='dry_run', value_type=DataType.YESNO)
                dry_run.read_from_file()
                source_value = source.check_status(cu).val
                destination_value = destn.check_status(cu).val
                interactive_value = inct.check_status(cu).val
                dry_run_value = dry_run.check_status(cu).val
                variables_dict = {"Source": source_value, "Destination": destination_value,
                                  "Interactive Mode": interactive_value, "Dry-run": dry_run_value}
                missing_values = [
                    key for key, var in variables_dict.items() if var == Status.MISSING.val]
                missing_values_str = ', '.join(missing_values)
                invalid_values = [
                    key for key, var in variables_dict.items() if var == Status.INVALID.val]
                invalid_values_str = ', '.join(invalid_values)
                m = ""
                if missing_values:
                    m += "Values are missing for:"+missing_values_str
                    m += "\n"

                if invalid_values:
                    m += "Values are invalid for:"+invalid_values_str

                if Status.NOT_EXISTS.val == source.check_status(cu).val:
                    m += "Source does not exist"

                if Status.AVAILABLE_FILE.val == destn.check_status(cu).val:
                    m += "Destination can't be a file"

                if Status.MISSING.val not in (source_value, destination_value) and source.value == destn.value:
                    m += "Your Source and destination path cannot be same."

                if m == "":
                    sync_command = ["rclone", os.environ.get(
                        "RCLONE_CONFIG_PATH", ""), "sync", source.value, destn.value]
                    if Status.ENABLED.val == inct.check_status(cu).val:
                        sync_command.insert(3, "-i")
                    else:
                        sync_command.insert(3, "-P")

                    if Status.ENABLED.val == dry_run.check_status(cu).val:
                        dry_run_command = sync_command[:]
                        dry_run_command.insert(4, "--dry-run")
                        print("Running dry run command :- ")
                        try:
                            subprocess.run(dry_run_command,
                                           shell=True, check=True)
                        except subprocess.CalledProcessError as e:
                            print(
                                f"Error running rclone command: {e.stderr.decode()}")
                        var = input(
                            "Press y to proceed with actual command execution: ")
                        if var in ("y", "Y"):
                            try:
                                subprocess.run(
                                    sync_command, shell=True, check=True)
                            except subprocess.CalledProcessError as e:
                                print(
                                    f"Error running rclone command: {e.stderr.decode()}")
                            print("Press any key to continue...")
                            cu.pause()
                    else:
                        try:
                            subprocess.run(
                                sync_command, shell=True, check=True)
                        except subprocess.CalledProcessError as e:
                            print(
                                f"Error running rclone command: {e.stderr.decode()}")
                        print("Press any key to continue...")
                        cu.pause()
                else:
                    print("Edit your profile and resolve the following issue :- \n"+m)
                    print("Press any key to continue...")
                    cu.pause()
            else:
                print("returning to menu ...")
                time.sleep(2)

        elif choice == "e":
            cu.clear_screen()
            message = ("Select a preset to edit :- ", f"No presets were found, copy-paste your preset ini file to {{}} and press R to refresh, press any other key to go back...", "going back...",
                       f"Presets were found, Select your desired preset, You can copy-paste your preset ini file to {{}} and press R to refresh, your new preset will be visible", "No selection was made, going back...")
            
            p_p = InputOutputFileOperations(
                prompt_message=message, search_directory=sync_path, search_extension=".ini")
            p_p.get_user_choice_from_console()
            if p_p.value is not None:
                cu.clear_screen()
                source = InputOutputFileOperations(
                    file_path=p_p.value, key='source', prompt_message='Enter your source path-> ', value_type=DataType.PATH)
                source.get_user_input_from_console()
                source.write_to_file()
                time.sleep(1)
                destn = InputOutputFileOperations(
                    file_path=p_p.value, key='destination', prompt_message='\n\nEnter your destination path->', value_type=DataType.PATH)
                destn.get_user_input_from_console()
                destn.write_to_file()
                time.sleep(1)
                inct = InputOutputFileOperations(
                    file_path=p_p.value, key='interactive', prompt_message='\n\nDo you want interactive method (Y/N)= ', value_type=DataType.YESNO)
                inct.get_user_input_from_console()
                inct.write_to_file()
                time.sleep(1)
                dry_run = InputOutputFileOperations(
                    file_path=p_p.value, key='dry_run', prompt_message='\n\nDo you want to dry run before proceeding (Y/N)= ', value_type=DataType.YESNO)
                dry_run.get_user_input_from_console()
                dry_run.write_to_file()
                time.sleep(1)
                cu.clear_screen()
                print("Profile updated with configurations.")
                time.sleep(1)
            else:
                print("returning to menu ...")
                time.sleep(2)

        elif choice == "d":
            cu.clear_screen()
            message = ("Select a preset to delete :- ", f"No presets were found, press enter to go back...", "going back...",
                       f"Presets were found, Select your preset for deletion", "No selection was made, going back...")
            p_p = InputOutputFileOperations(
                prompt_message=message, search_directory=sync_path, search_extension=".ini")
            p_p.get_user_choice_from_console()
            if p_p.value is not None:
                ffm.delete_file(p_p.value)
                print("File Deleted...")
                time.sleep(2)
            else:
                print("No file selected...")
                time.sleep(2)