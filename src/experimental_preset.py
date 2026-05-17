from Third_Party_Libs.tqdm import tqdm
import time
def testing_packageget():

    with open("Remove.xm",'r') as f:
        text = f.read().strip()
        section1_text, section2_text = text.split("<install>")
        InstallPackage_text = section1_text.split()
        RemovePackage_text = section2_text.split()
        pbar = tqdm(InstallPackage_text, desc="Install Packages", ascii=False, ncols=100)
        for pkg in pbar:
            pbar.set_postfix(current=pkg)
        print("Installing Packages")
        time.sleep(3)
        for pkg in RemovePackage_text:
            print(pkg)

testing_packageget()
