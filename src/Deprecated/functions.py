import os
import subprocess


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def install(package):
    subprocess.run(['adb', 'install', package], check=False)


def uninstall(package):
    subprocess.run(['adb', 'uninstall', package], check=False)


def force_uninstall(package):
    subprocess.run(['adb', 'shell', 'pm', 'uninstall', '-k', '--user', '0', package], check=False)


def makecfg():
    preset_dir = os.path.join(os.getcwd(), 'Preset')
    os.makedirs(preset_dir, exist_ok=True)
    main_file = os.path.join(preset_dir, 'main.xm')
    with open(main_file, 'a', encoding='utf-8'):
        pass
    return main_file
