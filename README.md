# Rclone Shorthands

**Use at your own risk. I am not responsible for any consequences.**

## About
**Rclone** is an open-source command-line program that provides a unified interface to manage files and directories across various cloud storage services and other remote file systems. It is designed to work with a wide range of cloud storage providers, making it a versatile tool for data synchronization, transfer, and backup. [Know More](https://rclone.org/)

Rclone is a command-line interface (CLI) tool that can be challenging for users less familiar with command line arguments and commands. Many general users, who only need to utilize a few features of Rclone, may find it daunting. To address this issue, we have developed a tool called **Rclone Shorthands**. This tool simplifies the usage of Rclone, especially for those who are not comfortable with the command line. It focuses on a preset-based system, allowing users to create profiles or presets for specific tasks. These presets can be executed whenever needed without the necessity of typing commands repeatedly.

**Rclone Shorthands** is also a command-line interface (CLI) tool, but it operates in a manner akin to selecting choices. It presents a menu of tasks along with their various presets, and the user simply has to make a selection.

## Limitations
- **The tool is still under development. Please check the notes for more information.**
- Encrypted .conf files are not yet supported. A workaround is to set the environment variable RCLONE_CONFIG_PASS=your_encryption_password and then start the tool.
- The tool is unable to differentiate between a path to a remote or local if the remote name consists of only a single alphabet. Try using a remote name with more than one alphabet or use a digit.
- The tool has been tested to run on most terminals in Windows, Linux, and Mac. However, it may not work as expected if an extremely rare terminal or shell is used. In such cases, Compatibility mode may help.
- Advanced tasks cannot be performed at the moment because there is no way to add additional arguments to the command created by the tool. The same limitation applies to filters.

## Compatibility Mode
We have implemented a **Compatibility Mode** in the tool. In some cases, the tool may not function correctly on the current terminal or shell. This mode allows users to utilize the tool on unsupported terminals or shells. We employ two terminal operations frequently to ensure a clean user experience. The first terminal operation is 'pause,' which holds the screen until the user presses a key. The second terminal operation is clearing the content of the terminal. It is possible that certain rarely used terminals or shells may not support one or both of these operations.

- If clearing the screen is not working properly, run the program with arguments like: launcher.py -c cls
- If the pause screen is not working properly, run the program with arguments like: launcher.py -c pause
- If both operations are not working properly, run the program with arguments like: launcher.py -c both

## Download
Currently, we do not provide a standalone executable for a specific operating system. Instead, you can download the zip file from the repository and use the main branch. Once the tool reaches a stable release, we will consider creating standalone executables.

## Installation & Quick Start
1. This tool does not require any formal installation process. Simply extract the downloaded zip file to an empty folder.
2. Ensure that you have Python version 3 or above installed.
3. Open the terminal within the folder where you extracted the program contents.
4. Type python launcher.py on Windows, or python3 launcher.py on Linux or Mac.

## Contributions
- Report bugs, ask questions and suggest new features by creating a new issue.
- Donate to [**Solifice**](https://linktr.ee/solifice).
- Donate to [**Hylence**](https://linktr.ee/hylence).

## Credits
1. Developers of rclone for creating such a powerful and versatile tool that has greatly contributed to the functionality of this project.
   - [rclone GitHub Repository](https://github.com/rclone/rclone)
   - [rclone Documentation](https://rclone.org/docs/)
2. This project is developed using the [Python programming language](https://www.python.org/), a versatile and powerful language that enables the creation of a wide range of applications.


## About us
[**Solifice**](https://github.com/Solifice) and [**Hylence**](https://github.com/Hylence) are college students who share a passion for technology. As tech enthusiasts and buddies, we enjoy using rclone because it's a free tool that allows us to sync our data between cloud and local storage devices. This tool is our college project, and while we are learning at a steady pace, we are committed to improving ourselves. We are uncertain about whether this tool will prove useful in the real world. However, if users discover and find value in this tool, we will do our best to support it. We have set different milestones, and we pledge to support this tool until at least those milestones are achieved.
