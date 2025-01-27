#!/usr/bin/python3
import os, sys, shutil, pathlib, json

homedir = os.path.expanduser("~")
xdg_config_path = os.path.join(homedir, ".config/electi-clangwrapper")
if not os.path.exists(xdg_config_path):
    os.makedirs(xdg_config_path)
target_prefix = "-".join(sys.argv[0].split("/")[-1].split("-")[:-1])

def check_tools_existance():
    tools = ["clang", "clang++", "ldid"]
    target_tools = [f"{target_prefix}-as", f"{target_prefix}-ld.real", f"{target_prefix}-strip", f"{target_prefix}-ar", f"{target_prefix}-ranlib"]
    for tool in tools:
        if not shutil.which(tool):
            print(f"Error: {tool} not found in PATH")
            sys.exit(1)
    for tool in target_tools:
        if not shutil.which(tool):
            print(f"Error: {tool} not found in PATH")
            sys.exit(1)

def get_linker_name():
    return f"{target_prefix}-ld.real"

def check_config_or_write():
    if not os.path.exists(os.path.join(xdg_config_path, f"{target_prefix}.json")):
        print(f"Config file does not exist, please specify SDK location for target {target_prefix}")
        with open(os.path.join(xdg_config_path, f"{target_prefix}.json"), "w") as f:
            sdk_ver, sdk_path = sdk_settings_input_loop()
            sdk_settings = {
                "sdk_version": sdk_ver,
                "sdk_path": sdk_path
            }
            json.dump(sdk_settings, f)
    else:
        with open(os.path.join(xdg_config_path, f"{target_prefix}.json"), "r") as f:
            sdk_settings = json.load(f)
            sdk_path = sdk_settings["sdk_path"]
            sdk_ver = sdk_settings["sdk_version"]
    return sdk_ver, sdk_path

def sdk_settings_input_loop():
    sdk_path = ""
    while not os.path.exists(sdk_path):
        sdk_path = input("SDK Path: ")
        sdk_settings_path = pathlib.Path(sdk_path) / "SDKSettings.plist"
        if not os.path.exists(sdk_settings_path.as_posix()):
            print(f"SDKSettings.plist not found in {sdk_path}")
            sdk_path = ""
        else:
            encounteredVersion = False
            sdk_ver = ""
            for line in open(sdk_settings_path, "r"):
                if encounteredVersion:
                    sdk_ver = line[line.find("ing>")+4:line.find("</s")]
                    break
                if "<key>Version</key>" in line:
                    encounteredVersion = True
    return sdk_ver, sdk_path

