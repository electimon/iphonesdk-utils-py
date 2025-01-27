#!/usr/bin/python3
import os, sys
from utils import check_tools_existance, get_linker_name, check_config_or_write

def main():
    check_tools_existance()
    check_config_or_write()
    args = []
    linking_binary = False
    command = get_linker_name()
    args.append(command)
    args = args + sys.argv[1:]
    if "crt1.3.1" in args or "-cpp" in args:
        linking_binary = True
    if linking_binary:
        if "-lc++" not in args:
            args.append("-lc++")
        if "-lc++abi" not in args:
            args.append("-lc++abi")
        if "-bind_at_load" in args:
            args.remove("-bind_at_load")
    if "-x" in args:
        sys.exit(1)
    os.execvpe(command, args, os.environ.copy())

main()

