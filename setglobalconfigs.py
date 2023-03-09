import globalfunctions

config = "_config_"
bisync_wkdir = "_bisync_wkdir_"
conf = "_conf_"
rclone= "_rclone_"
globalFile = "_global_Config_.txt"

configPath = globalfunctions.createPath(config, "")
rclonePath = globalfunctions.createPath(config, rclone)
globalFilePath = globalfunctions.createPath(config, globalFile)

isFirstRun = False
portableModeValue = None

if not globalfunctions.isDirPresent(configPath):
    globalfunctions.createDir(configPath)
    
if not globalfunctions.isDirPresent(rclonePath):
    globalfunctions.createDir(rclonePath)
    
if not globalfunctions.isFilePresent(globalFilePath):
    globalfunctions.createFile(globalFilePath)
    print("It seems you are using Rclone Shorthands for the First Time.\nYou need to configure it.\nThis is only a one time process.")
    isFirstRun = True
    
if isFirstRun:
    portableModeValue = globalfunctions.getValueFromUser("portableMode", "You want to use Portable Mode? :-", portableModeValue)
    globalfunctions.putValueToFile(globalFilePath, "portableMode", portableModeValue)