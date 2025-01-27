#!/usr/bin/python3
import os, sys
from utils import check_config_or_write, check_tools_existance, target_prefix

def main():
    check_tools_existance()
    sdk_ver, sdk_path = check_config_or_write()
    if "arm-" in target_prefix:
        sdk_arch = "armv6"
    elif "armv7-" in target_prefix:
        sdk_arch = "armv7"
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
#    args.append("-fno-integrated-as") // enable this and below for using apple's gas
#    args.append("-fno-asynchronous-unwind-tables")
    args.append("-D__ENVIRONMENT_MAC_OS_X_VERSION_MIN_REQUIRED__=1050")
    args.append("-Dstatic_assert=_Static_assert")
    args.append("-D_LIBCPP_REMOVE_TRANSITIVE_INCLUDES")
    args.append("-femulated-tls")
    if "Simulator" in sdk_path:
        args.append("-Oz")
        args.append("-Wl,-e,_main")
        args.append(f"-miphonesimulator-version-min={sdk_ver}")
        if command != "clang++": #and ("-dynamiclib" in args or "-bundle" in args):
            args.append(f"-lgcc_s.1")
    if command == "clang++":
        args.append("-std=c++11")
    args = args + sys.argv[1:]
    if command == "clang++":
        args.append("-Wl,-cpp")
        if "-dynamiclib" in args or "-bundle" in args:
            args.append("-lc++")
            args.append("-lc++abi")

    env_l = os.environ.copy()
    if "arm" in sdk_arch or "Simulator" in sdk_path:
        env_l["IPHONEOS_DEPLOYMENT_TARGET"] = sdk_ver
    else:
        env_l["MACOSX_DEPLOYMENT_TARGET"] = sdk_ver
    env_l["IOS_SIGN_CODE_WHEN_BUILD"] = "1"
    print(args)
    os.execvpe(command, args, env_l)

main()

