import subprocess
import os
from tuilb import *
from Third_Party_Libs.tqdm import tqdm
def ConnectADB():
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
    lines = result.stdout.splitlines()
    for line in lines[1:]:
        if "device" in line:
            return True
        elif "unauthorized" in line:
            return False
        else:
            return False
            
# The add functionality is WIP and wont be present in this release

def RemovePackageADB(remove):

    counter_packages_remove = 0
    counter_packages_skip = 0
    with open(remove,'r') as f:
        all_pkgs = [p for line in f for p in line.split()]

        
    pbar = tqdm(all_pkgs, desc="Removing Packages", unit="pkg")
    for packages1 in pbar:

            
        command = ["adb", "shell", "pm", "uninstall", "--user", "0", packages1]
        cmd = subprocess.run(command, capture_output=True, text=True, check=False)
        if "Success" in cmd.stdout:
            counter_packages_remove +=1 
#           prt(f"[+] Uninstalled: {packages1}",color="yellow",bold="True")
        else:
            counter_packages_skip +=1
#            prt(f"[-] Skipped: {packages1} (Not found or error)",color="yellow",bold=True)
#           print(cmd.stdout)

    subprocess.run("clear",shell=True)

    pbar.close()
    if counter_packages_remove >= 1:
        prt(f"Removed {counter_packages_remove} Packages with 0 errors!",color="green",bold=True)
    else:
        pass
    prt(f"{counter_packages_skip} are Skipped because they are not installed. [+]",color="yellow",bold="True")

#    with open(add,'r') as f2:
#        for ln in f2:
#            pck = ln.strip()
#            print(pck)
    


    
#print(ConnectADB())

#RemovePackageADB("Remove.xm")
