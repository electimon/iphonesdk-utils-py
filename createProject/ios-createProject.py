#!/usr/bin/env python3

from pathlib import Path
import argparse
from datetime import datetime
from jinja2 import Environment

script_dir = Path(__file__).resolve().parent

def createProject(projectName, organizationName, authorName):
    env = Environment()
    Path(projectName).mkdir(parents=True, exist_ok=True)
    for file in Path(script_dir / 'templates').rglob('*'):
        if file.is_file():
            content = env.from_string(file.read_text())
            _file = Path(projectName) / file.name.replace('.jinja2', '')
            _file.write_text(content.render(
                project_name=projectName,
                organization_name=organizationName,
                author_name=authorName,
                date=datetime.now().strftime('%Y-%m-%d')
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