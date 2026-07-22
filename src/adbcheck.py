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

# The add functionality is WIP and won't be present in this release

def RemovePackageADB(remove):
    counter_packages_remove = 0
    counter_packages_skip = 0

    # Read packages, skipping comment lines and inline comments
    all_pkgs = []
    with open(remove, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Strip inline comments (anything after a '#')
            if '#' in line:
                line = line.split('#', 1)[0].strip()
            # Split the line into package names (space-separated)
            for p in line.split():
                if p:   # ignore empty strings
                    all_pkgs.append(p)

    pbar = tqdm(all_pkgs, desc="Removing Packages", unit="pkg")
    for packages1 in pbar:
        command = ["adb", "shell", "pm", "uninstall", "--user", "0", packages1]
        cmd = subprocess.run(command, capture_output=True, text=True, check=False)
        if "Success" in cmd.stdout:
            counter_packages_remove += 1
        else:
            counter_packages_skip += 1

    subprocess.run("clear", shell=True)
    pbar.close()

    if counter_packages_remove >= 1:
        prt(f"Removed {counter_packages_remove} Packages with 0 errors!", color="green", bold=True)
    prt(f"{counter_packages_skip} are Skipped because they are not installed. [+]", color="yellow", bold="True")
