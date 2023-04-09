import getpass
import subprocess
import os
import sys
from colorama import init, Fore, Style

        
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
        print(f"{Fore.LIGHTYELLOW_EX}  You didn't provide any value, Skipping.{Style.RESET_ALL}")
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