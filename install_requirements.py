import glob
import subprocess
import sys
from typing import List
import argparse


DEFAULT_CORE_REQUIREMENTS_FILE = './dev-requirements.txt'

parser = argparse.ArgumentParser(description="A utility to install OSIS project requirements.")
parser.add_argument(
    "-c",
    "--core",
    help="core requirements file (default: dev-requirements.txt)",
    default=DEFAULT_CORE_REQUIREMENTS_FILE,
    type=str,
    metavar="FILE"
)

args = parser.parse_args()


def install(core_file: str) -> None:
    install_requirement(core_file)
    install_app_requirements()


def install_app_requirements():
    app_requirements = find_app_requirements()
    for requirement in app_requirements:
        install_requirement(requirement)


def find_app_requirements() -> List[str]:
    return [file for file in glob.glob("./*/requirements.txt")]


def install_requirement(path: str) -> None:
    subprocess.run(
        ["pip", "install", "-r",  path],
        stdout=sys.stdout,
        stderr=sys.stderr,
        universal_newlines=True,
    )


install(args.core)
