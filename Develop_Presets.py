#Maintainer: @Thvrett77
#Last Modified 10/6/26

# !!!!!WORK IN PROGRESS DO NOT USE UNLESS YOU ARE A DEVELOPER AND FIX THIS MESS OF A SCRIPT!!!!!


import time
import subprocess
import argparse
# adb shell getprop ro.build.version.release  OUTPUT: INT
# adb shell getprop ro.product.device: (codename)
# adb shell getprop ro.product.manufacturer: (Manufacturer)
# adb shell getprop ro.product.marketname: (Device Model)
# adb shell getprop ro.mi.os.version.incremental: (OS version)




def Commands_exec(command):
    result = subprocess.run(command, capture_output=True,shell=True,text=True)
    return result.stdout,result.stderr

Data = {
    "Android_Version": "adb shell getprop ro.build.version.release",
    "Codename": "adb shell getprop ro.product.device",
    "Manufacturer": "adb shell getprop ro.product.manufacturer",
    "Model": "adb shell getprop ro.product.marketname",
    "Os_Version": "adb shell getprop ro.mi.os.version.incremental"
}




def Build_Enviroment():
    dr_name = Commands_exec(Data["Codename"])
    Os_ver = Commands_exec(Data["Os_Version"])
    nm = Commands_exec(Data["Model"])
    nm = nm[0].strip()
    dr_name = dr_name[0].strip()
    Os_ver = Os_ver[0].strip()
    debug = Commands_exec(f"mkdir {dr_name} && cd {dr_name} && touch {Os_ver}.txt")
    maintainer = input("Maintainer: ")
    

    with open(f"{dr_name}/{Os_ver}.txt", "w", encoding="utf-8") as preset_file:
        preset_file.write(f"#Maintainer: {maintainer}\n#Phone Preset: {nm}\n\n\n #====Here You Will Put Some Packages That You Find Bloat====\n")
    


def Get_Device_Info():
    global data
    for key,value in Data.items():
        vl = Commands_exec(value)
        vl = vl[0].strip()
        print(f"{key}:{vl}")
    w = input("Would You Like To Make A preconfigured enviroment Based Off the Detected Data? (Y/N):")
    if w.upper() == "Y":
        pass
    else:
        return

 
# Debug

#Get_Device_Info()
#Build_Enviroment()
