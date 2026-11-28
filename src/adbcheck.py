#Maintainer: @Thvrett77
# Last Updated: 2026-02-10 (yyyy-mm-dd)
# Changed: Replaced the tqdm loading bar with the GUI approach one found in experimental_GUI.py

# To Be implemented
# This needs to be done because some apps when tried to be removed result in an error (Failure [-1000])
# adb shell pm disable-user --user 0 



import os
import subprocess
import time
import check_download_presets
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def ConnectADB():
    subprocess.run("adb kill-server")
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=False,shell=True)
    lines = result.stdout.splitlines()
    for line in lines[1:]:
        if 'device' in line.lower() and 'device' in line.lower():
            print("ADB Connected Successfully! [+]")
            return True
        if 'unauthorized' in line.lower():
            print("ADB Unauthorized! [-]")
            time.sleep(0.5)
            return False
                    
    return False


# The add functionality is WIP and won't be present in this release

def RemovePackageADB(remove, progress_callback=None):
    """Remove packages from a preset file or package-list string."""
    if not isinstance(remove, (str, os.PathLike)):
        raise TypeError("remove must be a file path or package-list string")

    counter_packages_remove = 0
    counter_packages_skip = 0

    is_path = (
        isinstance(remove, os.PathLike)
        or os.path.isfile(remove)
        or os.path.sep in remove
        or (os.path.altsep is not None and os.path.altsep in remove)
    )
    if is_path:
        with open(remove, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    else:
        lines = remove.splitlines()

    # Read packages, skipping comment lines and inline comments
    all_pkgs = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '#' in line:
            line = line.split('#', 1)[0].strip()
        for p in line.split():
            if p:
                all_pkgs.append(p)

#    pbar = tqdm(all_pkgs, desc='Removing Packages', unit='pkg')
    for package_index, package in enumerate(all_pkgs, start=1):
        command = ['adb', 'shell', 'pm', 'uninstall', '--user', '0', package]
        cmd = subprocess.run(command, capture_output=True, text=True, check=False)

        if 'Success' in cmd.stdout:
            counter_packages_remove += 1
        else:
            counter_packages_skip += 1

        if progress_callback is not None:
            progress_callback(package_index, len(all_pkgs), package)

    clear_console()
    #    pbar.close()

    MSG = f"Removed {counter_packages_remove} Packages with 0 errors!"
#        prt(f'Removed {counter_packages_remove} Packages with 0 errors!', color='green', bold=True)
    Warn = f'{counter_packages_skip} are Skipped because they are not installed. [+]'
#    prt(f'{counter_packages_skip} are Skipped because they are not installed. [+]', color='yellow', bold='True')

    return MSG, Warn

#RemovePackageADB(r"C:\Users\Thanasis\Documents\Projects\Omni_Debloat\Omni_Debloat-main\Presets\tanzanite\3.0.302.0.WOGEUXM.xm")

#RemovePackageADB(check_download_presets.Get_Content_Out_Of_CDN("temp_list.json"))
# Debug Purposes ONLY


#ConnectADB()