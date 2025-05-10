import csv
import os
# Interprets a string as a boolean. Returns True or False
def parseBool(string:str|bool, silent:bool=False):
    if type(string) == str:
        if string.lower() == 'true':
            return True
        elif string.lower() == 'false':
            return False
        else:
            if not silent:
                raise ValueError(f'Invalid value "{string}". Must be "True" or "False"')
            elif silent:
                return string
    elif type(string) == bool:
        if string == True:
            return True
        elif string == False:
            return False
    else:
        raise ValueError('Not a valid boolean string')
    
def parseConfigSetting(setting) -> str | int | bool:
    # Remove any quotes user may have added in config file
    setting = setting.strip("\"").strip("\'")

    # Check if it is a boolean
    if type(parseBool(setting, silent=True)) == bool:
        return parseBool(setting, silent=True)

    # Check if it is an integer
    try:
        return int(setting)
    except ValueError:
        pass

    # Otherwise return the string in lower case
    return setting.lower()

# Returns a list of dictionaries from a csv file. Where the key is the column name and the value is the value in that column
# The column names are set by the first row of the csv file
def csv_to_dictList(csvFilePath:str) -> list[dict[str,str]]:
    with open(csvFilePath, "r", encoding='utf-8-sig') as data:
        entriesDictsList:list[dict[str,str]] = []
        for line in csv.DictReader(data):
            entriesDictsList.append(line)
    return entriesDictsList

# Returns a list of strings from a txt file. Ignores empty lines and lines that start with '#'
def txt_to_list(txtFilePath:str) -> list[str]:
    with open(txtFilePath, "r", encoding='utf-8-sig') as data:
        entriesList:list[str] = []
        for line in data:
            if line.strip() != '' and line.strip()[0] != '#':
                entriesList.append(line.strip())
    return entriesList


# User inputs Y/N for choice, returns True or False. Takes in message to display
# 
def choice(message:str="", bypass:bool=False, allowNone:bool=False):  
  if bypass == True:
    return True

  # While loop until valid input
  valid = False
  while valid == False:
    response = input("\n" + message + f" (y/n): ").strip()
    if response == "Y" or response == "y":
      return True
    elif response == "N" or response == "n":
      return False
    elif (response == "X" or response == "x") and allowNone == True:
      return None
    else:
      print("\nInvalid Input. Enter Y or N  --  Or enter X to return to main menu.")  
      
      
def getFirstAvailableFileName(directoryPath:str, fileNameBase:str, extension:str) -> str:
    """
    Returns the first available file name in the directory with the given base name and extension.
    If the file already exists, it will append a number to the base name until an available name is found.
    """
    # Check if directory exists
    if not os.path.exists(directoryPath):
        os.makedirs(directoryPath)

    # Check if file already exists
    fileName = f"{fileNameBase}.{extension}"
    filePath = os.path.join(directoryPath, fileName)
    i = 2
    while os.path.exists(filePath):
        fileName = f"{fileNameBase}_{i}.{extension}"
        filePath = os.path.join(directoryPath, fileName)
        i += 1

    return filePath