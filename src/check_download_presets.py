#Maintainer: @Thvrett77
#Last Modified 11/21/26

import AI_Develop_Presets
import requests
import json

# Variables to help new contributors
#codename = it returns the device codename required for downloading the correct preset

"""
For Those who wonder why i code in 3 functions instead of one big efficient one, is because 
i can manage this kind of code more easier and also it is better for updating some parts of the code
Hope you understand me!

"""

def Get_Device_Codename():
    manager = AI_Develop_Presets.DevicePresetManager()
    codename, error = manager.execute_command(manager.Data["Codename"])
    if error or not codename:
        message = (
            f"Unable to retrieve device codename: {error}"
            if error
            else "No device codename was returned by ADB."
        )
        raise RuntimeError(message)
    return codename

def Fetch_Presets(file):
    with open(file,'r') as f:
        try:
            a = json.load(f)
            fallback_to_universal = a["universal"]["link"]
            Preset = a[Get_Device_Codename()]["link"] 
        except KeyError:
            return fallback_to_universal
        except RuntimeError:
            return "Device is Not Connected"
        return Preset
    
def Get_Content_Out_Of_CDN(ff):
    url = Fetch_Presets(ff)
    if url == "Device is Not Connected":
        raise RuntimeError("Could not detect the device codename. Check the ADB connection.")

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text

# ---- For Debug Purposes Only ----


#Get_Content_Out_Of_CDN("temp_list.json")
#Fetch_Presets("temp_list.json")
