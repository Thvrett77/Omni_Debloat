from tuilb import fancy_input, prt, print_with_color
import subprocess
import time
import functions
import os
import adbcheck
import sys
from Third_Party_Libs.tqdm import tqdm


ascii_greet = r""" $$$$$$\  $$\      $$\ $$\   $$\ $$$$$$\ 
$$  __$$\ $$$\    $$$ |$$$\  $$ |\_$$  _|
$$ /  $$ |$$$$\  $$$$ |$$$$\ $$ |  $$ |  
$$ |  $$ |$$\$$\$$ $$ |$$ $$\$$ |  $$ |  
$$ |  $$ |$$ \$$$  $$ |$$ \$$$$ |  $$ |  
$$ |  $$ |$$ |\$  /$$ |$$ |\$$$ |  $$ |  
 $$$$$$  |$$ | \_/ $$ |$$ | \$$ |$$$$$$\ 
 \______/ \__|     \__|\__|  \__|\______|
                                         
                                         
                                         """ 


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')



def Details():
    time.sleep(1)
    clear_console()
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
    try:
        clear_console()
        global ascii_greet
        prt(text=ascii_greet,color="white",bold=True)
        prt(text="Welcome To Omni Android Debloater!!!!",color="purple",bold=True)
        time.sleep(2)
        clear_console()
        prt("Checking if your device is connected [!]",color="yellow",bold=True)
        start_time = time.time()
        timeout = 15
        while True:
            try:
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    prt("Reached Timeout Stopping [X]",color="yellow",bold=False)
                    time.sleep(4)
                    clear_console()
                    return
                if adbcheck.ConnectADB() == True:
                    prt("Device Connected [+]",color="green",bold=True)
                    time.sleep(0.5)
                    clear_console()
                    break
                else:
                    prt("Device Failed To Connect [-]",color="red",bold=True)
                    time.sleep(0.2)
            except KeyboardInterrupt:
                 prt("Program Terminated Forcefully",color="white",bold=True)
                 sys.exit(0)




        xm_path = Details()

        prt("Removing Packages That The Preset Specified [+]",color="green",bold=True)
    
        areyousure = fancy_input("Are You Sure You Want To Continue? (Y/N)",color="aqua",bold=True)
        if areyousure == "N".lower():
            return
        adbcheck.RemovePackageADB(xm_path)
        sys.exit(0)


    except KeyboardInterrupt:
        raise

    
    
# These are commented because they were causing a bug so i moved them into the try and except block to fix its
            
        

#    xm_path = Details()

#    prt("Removing Packages That The Preset Specified [+]",color="green",bold=True)
    
#    areyousure = fancy_input("Are You Sure You Want To Continue? (Y/N)",color="aqua",bold=True)
#    if areyousure == "N".lower():
#        return
#    adbcheck.RemovePackageADB(xm_path)
 #   sys.exit(0)

try:
    main()
except KeyboardInterrupt:
    prt("Program Terminated Forcefully",color="white",bold=True)
    sys.exit()
