import subprocess

def install (package):
    subprocess.run(['adb', 'install', package])

def uninstall (package):
    subprocess.run(f"adb uninstall {package}")

def force_uninstall (package):
    subprocess.run(f"adb shell pm uninstall -k --user 0 {package}")

def makecfg ():
    subprocess.run(["mkdir","Preset"],shell=True)
    subprocess.run("type nul > Preset\\main.xm", shell=True)
