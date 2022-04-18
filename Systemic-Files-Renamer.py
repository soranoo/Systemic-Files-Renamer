# projest start on 25-03-2022
# author Freeman
project_name = "Systemic Files Renamer"
project_version = "1.0.0"
project_author = "Freeman"
project_start_date = "25-03-2022"
project_last_update = "26-03-2022"


import os
import time

from datetime import datetime

try:
    import pyfiglet 
    from rich.progress import track
    from rich.traceback import install
    from rich import print as cprint
    from colorama import init
except ImportError as err:
    print(f"Missing dependency: {err}. Would you like to install it now? [y/n]")
    o = input()
    if o.lower() == "y":
        print("Installing...")
        os.system("pip install rich")
        os.system("pip install colorama")
        os.system("pip install pyfiglet")
        print("\n\nThe installation is done.")
        print("Restarting program...")
        os.system(f"py {__file__}")
        exit()
    else:
        print("Please install missing dependency before continue.")
        print("The program will shut down after 10s...")
        time.sleep(10)
        exit()


init()
install(show_locals=True)

id_prefix = "ID"
input_folder_path = None
last_id = 0

class Colorcode:
    reset = '\x1b[0m'
    bold = '\x1b[1m'
    dim = '\x1b[2m'
    red = '\x1b[31m'
    green = '\x1b[32m'
    yellow = '\x1b[33m'
    blue = '\x1b[34m'
    magenta = '\x1b[35m'
    cyan = '\x1b[36m'
    white = '\x1b[37m'
    gray = '\x1b[90m'

def print_tips(msg, symbol = "!", symbolColor = Colorcode.red, mainMsgColor = Colorcode.blue):
    print(f"{symbolColor}{Colorcode.bold}[{symbol}]{Colorcode.reset} {mainMsgColor}{Colorcode.bold}{msg}{Colorcode.reset}")

def create_path(path):
    if not os.path.isdir(path):
        # create input folder
        os.mkdir(os.path.join(os.getcwd(), path))
    return path

def init():
    global input_folder_path
    global id_prefix
    global last_id
    input_folder_path = create_path(os.path.join(os.getcwd(), "input"))

    print_tips("Put the files in the folder you want to rename.")
    print_tips(f"Here's the input folder path: {input_folder_path}")
    print_tips("The file ID will given according to the last modified date.")
    o = input(f"\nDo you want to change the ID prefix, current: <{id_prefix}>? [y/n] ")
    if o.lower() == "y":
        id_prefix = input(f"Please input the new ID prefix: ")
    print_tips(f"All Done~ The ID will look like: {id_prefix}6489", symbol = "ok", symbolColor = Colorcode.green, mainMsgColor = Colorcode.cyan)
    last_id = int(input("\nEnter the last capture ID: "))

def form_id_structure(id):
    return id_prefix + str(id)


def main():
    def getFiles():
        return os.listdir(os.path.join(os.getcwd(), input_folder_path))

    def reorderFileByModifiedDate(files):
        lastModifiedDate = dict()
        # get last modified date of each file
        for file in files:
            filePath = os.path.join(os.getcwd(), input_folder_path, file)
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filePath) # ref: https://stackoverflow.com/a/237084
            lastModifiedDate[file] = time.ctime(mtime)
        # reorder the file list by last modified date
        files = sorted(files, key=lambda file: datetime.strptime(lastModifiedDate[file], "%a %b %d %H:%M:%S %Y")) # ref: Sat Dec 18 09:04:43 2021, https://strftime.org/
        return files

    def renameFiles(files, filePrefix = ""):
        if len(files) == 0:
            print("No files found.")
            return False
        files = reorderFileByModifiedDate(files)
        currentID = last_id
        # loop through the input folder and rename the files accordingly
        for file in track(files):
            currentID += 1
            # get the file path
            filePath = os.path.join(os.getcwd(), input_folder_path, file)
            
            # get file extension
            file_extension = os.path.splitext(filePath)[1]
            # rename the file
            os.rename(filePath, os.path.join(os.getcwd(), input_folder_path, filePrefix + form_id_structure(currentID) + file_extension))

    startTime = time.time()

    # rename files to temp file to avoid file name overlap
    renameFiles(getFiles(), filePrefix = "[temp]")
    # rename files to fit the naming pattern
    renameFiles(getFiles(), filePrefix = "")

    # calaculate the time taken
    endTime = time.time()

    filesCount = len(getFiles())
    # print and round the time to 5 decimal places
    print(f"{Colorcode.green}Time taken: {round(endTime - startTime, 5)}s for {filesCount} files.{Colorcode.reset}")
    print(f"ID range: {last_id + 1} - {last_id + filesCount}")

if __name__ == "__main__":    
    # welcome message
    cprint(pyfiglet.figlet_format(project_name))
    print(f"{Colorcode.gray}Projest start on {project_start_date}    Last modified: {project_last_update}")
    print(f"Version: {project_version}")
    print(f"Created by {project_author}{Colorcode.reset}\n\n")

    while True:
        init()
        main()
        print("\n\n")
        o = input("Do you want to rename more files? [y/n] ")
        if o.lower() == "n":
            break
        else:
            print("\n\n")
            continue
    print("The program will shut down after 5s...")
    time.sleep(5)
    exit()
