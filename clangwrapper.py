#!/usr/bin/python3
import os, sys, shutil, pathlib, json

homedir = os.path.expanduser("~")
xdg_config_path = os.path.join(homedir, ".config/electi-clangwrapper")
if not os.path.exists(xdg_config_path):
    os.makedirs(xdg_config_path)
target_prefix = "-".join(sys.argv[0].split("/")[-1].split("-")[:-1])

def main():
    check_tools_existance()
    sdk_ver, sdk_path = check_config_or_write()
    if "arm-" in target_prefix:
        sdk_arch = "armv6"
    else:
        sdk_arch = "i386"
    args = []
    command = ""
    if "++" in sys.argv[0]:
        command = "clang++"
    else:
        command = "clang"
    args.append(command)
    args.append("-target")
    args.append(target_prefix)
    args.append("-arch")
    args.append(sdk_arch)
    args.append("-isysroot")
    args.append(sdk_path)
    args.append("-mlinker-version=134.9")
    args = args + sys.argv[1:]

    env_l = os.environ.copy()
    env_l["IPHONEOS_DEPLOYMENT_TARGET"] = sdk_ver
    env_l["IOS_SIGN_CODE_WHEN_BUILD"] = "1"
    os.execvpe(command, args, env_l)

def check_tools_existance():
    tools = ["clang", "clang++", "ldid"]
    target_tools = [f"{target_prefix}-as", f"{target_prefix}-ld", f"{target_prefix}-strip"]
    for tool in tools:
        if not shutil.which(tool):
            print(f"Error: {tool} not found in PATH")
            sys.exit(1)
    for tool in target_tools:
        if not shutil.which(tool):
            print(f"Error: {tool} not found in PATH")
            sys.exit(1)

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
                if "Version" in line:
                    encounteredVersion = True
    return sdk_ver, sdk_settings_path.as_posix()

main()

