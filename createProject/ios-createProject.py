#!/usr/bin/env python3

import json
import os
from pathlib import Path
import argparse
from datetime import datetime
from jinja2 import Environment

script_dir = Path(__file__).resolve().parent
homedir = os.path.expanduser("~")
xdg_config_path = os.path.join(homedir, ".config/electi-clangwrapper")

def createProject(projectName, organizationName, authorName):
    env = Environment()
    Path(projectName).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(xdg_config_path):
        print(f"Config file does not exist, please run either your linker or clang :(")
        sys.exit(1)
    config = json.load(open(os.path.join(xdg_config_path, f"arm-apple-darwin9.json"), "r"))
    for file in Path(script_dir / 'templates').rglob('*'):
        if file.is_file():
            content = env.from_string(file.read_text())
            _file = Path(projectName) / file.name.replace('.jinja2', '')
            _file.write_text(content.render(
                project_name=projectName,
                organization_name=organizationName,
                author_name=authorName,
                date=datetime.now().strftime('%Y-%m-%d'),
                sdk_version=config['sdk_version'],
                sdk_path=config['sdk_path']
            ))

def main():
    parser = argparse.ArgumentParser(description='Create a new iOS application')
    parser.add_argument('projectName', type=str, help='Name of the project')
    parser.add_argument('organizationName', type=str, help='Name of the organization')
    parser.add_argument('authorName', type=str, help='Name of the author')
    args = parser.parse_args()
    createProject(args.projectName, args.organizationName, args.authorName)

if __name__ == '__main__':
    main()