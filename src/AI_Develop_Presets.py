# Maintainer: @Thvrett77, Qwen 3.0:8b
# Last Modified 11/16/26

import time
import subprocess
import argparse
import os

class DevicePresetManager:
    def __init__(self):
        self.Data = {
            "Android_Version": "adb shell getprop ro.build.version.release",
            "Codename": "adb shell getprop ro.product.device",
            "Manufacturer": "adb shell getprop ro.product.manufacturer",
            "Model": "adb shell getprop ro.product.marketname",
            "Os_Version": "adb shell getprop ro.mi.os.version.incremental"
        }
        self.device_info = {}
        
    def execute_command(self, command):
        result = subprocess.run(command, capture_output=True, shell=True, text=True)
        return result.stdout.strip(), result.stderr.strip()
    
    def get_device_info(self):
        self.device_info = {}
        for key, value in self.Data.items():
            stdout, stderr = self.execute_command(value)
            if stderr:
                print(f"Error retrieving {key}: {stderr}")
            else:
                self.device_info[key] = stdout
        
        # Ask user if they want to create a preset
        choice = input("Would you like to create a preconfigured environment based on detected data? (Y/N): ")
        if choice.upper() == "Y":
            self.create_preset_environment()
    
    def create_preset_environment(self):
        if not self.device_info:
            print("No device information available to create preset")
            return
            
        codename = self.device_info.get("Codename", "unknown")
        os_version = self.device_info.get("Os_Version", "unknown")
        dir_name = f"{codename}_{os_version}"
        
        try:
            os.makedirs(dir_name, exist_ok=True)
            file_path = os.path.join(dir_name, f"{os_version}.txt")
            
            with open(file_path, "w", encoding="utf-8") as preset_file:
                preset_file.write(f"# Maintainer: {input('Maintainer: ')}\n")
                preset_file.write(f"# Phone Preset: {self.device_info.get('Model', 'unknown')}\n\n")
                preset_file.write("#====Here You Will Put Some Packages That You Find Bloat====\n")
                
            print(f"Preset environment created at {file_path}")
        except Exception as e:
            print(f"Error creating preset environment: {str(e)}")
    
    def debug(self):
        print("Debug information:")
        for key, value in self.device_info.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    manager = DevicePresetManager()
    manager.get_device_info()
    manager.debug()