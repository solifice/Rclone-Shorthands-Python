import getpass
import subprocess
import os
import sys

def getCurrentPath():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        return os.path.dirname(os.path.abspath(__file__))
        
def createPath(relativePath, fileName):
    return os.path.join(getCurrentPath(), relativePath, fileName)

def isFilePresent(filePath):
    if os.path.isfile(filePath):
        #print("The file", filePath, "exists.")
        return True
    else:
        #print("The file", filePath, "does not exist.")
        return False
        
def isDirPresent(folderPath):
    if os.path.isdir(folderPath):
        #print("The folder", folderPath, "exists.")
        return True
    else:
        #print("The folder", folderPath, "does not exist.")
        return False
        
def createDir(folderPath):
    try:
        os.makedirs(folderPath)
    except OSError as e:
        print(f"Unable to create directory: {e}")

def createFile(filePath):
    try:
        with open(filePath, 'w') as f:
            pass
        #print(f"Empty file created at {filePath}")
    except Exception as e:
        print(f"Error creating file: {e}")
        
def getValueFromFile(filePath, variableName):

    try:
        with open(filePath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if variableName in line:
                    variableValue = line.split('=')[1].strip()
                    if variableValue == '':
                        return None
                    variableValue = variableValue.strip()
                    return variableValue
    except FileNotFoundError:
        pass
    return None
    
def getValueFromUser(variableName, prompt, existingValue):

    variableValue = input(prompt)
    if variableValue.strip() == '':
        print(f"You didn't provide any value for {variableName}. Skipping update.")
        return existingValue
    return variableValue.strip()
    
def putValueToFile(filePath, variableName, variableValue):

    if isValueAvailable(variableValue):
        try:
            with open(filePath, 'r') as f:
                lines = f.readlines()

            isVariablePresent = False
            for i, line in enumerate(lines):
                if line.startswith(variableName + '='):
                    variableValue = variableValue.strip()
                    lines[i] = f"{variableName}={variableValue}\n"
                    isVariablePresent = True
                    break
            if not isVariablePresent:
                lines.append(f"{variableName}={variableValue}\n")

            with open(filePath, 'w') as f:
                f.writelines(lines)

        except Exception as e:
            print(f"Error writing to file: {e}")

def isValueAvailable(variableValue):
    
    return variableValue is not None
        
#---------------------------------------------------------------------------------------------------------------------