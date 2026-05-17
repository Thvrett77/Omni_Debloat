from tuilb import fancy_input, prt, print_with_color
import subprocess
import time
from rq2b_xm_maker import xm_groups_to_json, CheckSecondGroupHasHttpsValidDownloads
import functions
import os
import adbcheck
import sys
from Third_Party_Libs.tqdm import tqdm
ascii_greet = r"""                           /$$                     /$$       /$$             /$$           /$$       /$$                       /$$                        
                          | $$                    |__/      | $$            | $$          | $$      | $$                      | $$                        
  /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$  /$$  /$$$$$$$        /$$$$$$$  /$$$$$$ | $$$$$$$ | $$  /$$$$$$   /$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$ 
 |____  $$| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$| $$ /$$__  $$       /$$__  $$ /$$__  $$| $$__  $$| $$ /$$__  $$ |____  $$|_  $$_/   /$$__  $$ /$$__  $$
  /$$$$$$$| $$  \ $$| $$  | $$| $$  \__/| $$  \ $$| $$| $$  | $$      | $$  | $$| $$$$$$$$| $$  \ $$| $$| $$  \ $$  /$$$$$$$  | $$    | $$$$$$$$| $$  \__/
 /$$__  $$| $$  | $$| $$  | $$| $$      | $$  | $$| $$| $$  | $$      | $$  | $$| $$_____/| $$  | $$| $$| $$  | $$ /$$__  $$  | $$ /$$| $$_____/| $$      
|  $$$$$$$| $$  | $$|  $$$$$$$| $$      |  $$$$$$/| $$|  $$$$$$$      |  $$$$$$$|  $$$$$$$| $$$$$$$/| $$|  $$$$$$/|  $$$$$$$  |  $$$$/|  $$$$$$$| $$      
 \_______/|__/  |__/ \_______/|__/       \______/ |__/ \_______/       \_______/ \_______/|_______/ |__/ \______/  \_______/   \___/   \_______/|__/      
                                                                                                                                                          
                                                                                                                                                          
                                                                                                                                                          """


def advanced_mode():
    help = "Advanced Mode: \n 1. rm (com.package.example) # Removes a package forcefully even if its not uninstallable" \
    "\n 2. install (filename.apk) # Installs an apk package to the phone " \
    "\n 3. makecfg # Builds the files essential for user made presets \n 4. build # Builds the .xm file to a file that the program understands \n 5. clear # Clears the terminal \n 6. help # Displays this you are reading\n 7. exit # This one is obvious"
    prt(text=help,bold=True,color="blue")
    time.sleep(0.2)
    while True:
        time.sleep(0.1)
        Test = fancy_input("Shell",color="red",bold=True)
        if Test == "EXIT".lower():
            break
        elif Test == "MAKECFG".lower():
            functions.makecfg()
            prt(text="Made Config File!",color="blue",bold=True)
        elif Test == "CLEAR".lower():
            subprocess.run("clear",shell=True)
        elif Test == "HELP".lower():
            prt(text=help,bold=True,color="blue")
        elif Test.startswith("INSTALL".lower()):
            path = Test[8:]
            if len(path) < 1 or not path.endswith(".apk") or not os.path.isfile(path):
                prt(text="Invalid APK file, Or Directory [x]",color="red",bold=True)
            else:
                print(path)
        elif Test.startswith("RM".lower()):
            package = Test[2:].strip()
            print(package)
            if len(package) < 1:
                print("No Output")
            



def Details():
    time.sleep(1)
    subprocess.run("clear",shell=True)
    prt(text="Select the xm preset thats from the official github",color="blue",bold=True)
    inp = fancy_input(text="Enter The .xm path here example (Desktop\yourpreset.xm)",color="green",bold=True)
    if len(inp) < 2 or not os.path.isfile(inp):
        prt("File does not exist [X]",bold=True,color="red")
        return Details()
    elif not inp.endswith(".xm"):
        prt("That File Is Not Valid [X]",bold=True,color="red")
        return Details()
    else:
        return inp



def main():
    subprocess.run("clear",shell=True)
    global ascii_greet
    prt(text=ascii_greet,color="blue",bold=True)
    prt(text="Welcome To Thvretts Universal Android Debloater!!!!",color="purple",bold=True)
    mode = fancy_input("Would you like to enter advanced mode? (Y/N)",color="blue",bold=True)
    if mode == "Y".lower():
        advanced_mode()
    time.sleep(0.4)
    subprocess.run("clear",shell=True)
    prt("Checking if your device is connected [!]",color="yellow",bold=True)
    start_time = time.time()
    timeout = 15
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            prt("Reached Timeout Stopping [X]",color="yellow",bold=False)
            time.sleep(4)
            subprocess.run("clear",shell=True)
            return
        if adbcheck.ConnectADB() == True:
            prt("Device Connected [+]",color="green",bold=True)
            time.sleep(0.5)
            subprocess.run("clear",shell=True)
            break
        else:
            prt("Device Failed To Connect [-]",color="red",bold=True)
            time.sleep(0.2)
    
    
            
        

    xm_path = Details()

    prt("Removing Packages That The Preset Specified [+]",color="green",bold=True)
    
    areyousure = fancy_input("Are You Sure You Want To Continue? (Y/N)",color="aqua",bold=True)
    if areyousure == "N".lower():
        return
    adbcheck.RemovePackageADB(xm_path)
    prt("All Done You May Enjoy Your Debloated Phone!",color="green",bold=True)


main()
