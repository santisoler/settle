"""
Main function for running Settle
"""
import os
import sys
import subprocess
import yaml
import inquirer
import platform
from inquirer.themes import load_theme_from_dict

from . import package_managers
from .package_managers import get_package_manager
from .distros import DISTROS_PACKAGE_MANAGERS, PACKAGE_MANAGERS
from .argparser import create_argparser
from .questions import Asker


def main():
    # Parse command line arguments
    parser = create_argparser()
    arguments = parser.parse_args()

    # Read packages.yml and get defaults
    packages = yaml.load(arguments.packages, Loader=yaml.FullLoader)

    # Get package manager class
    package_manager = get_package_manager()

    # Ask questions
    asker = Asker(packages, package_manager)
    answers = asker.ask_questions()

    # Continue only if the last confirmation question is true
    if not answers["continue"]:
        sys.exit()

    # Initialize package manager
    if "package_manager" in answers:
        package_manager = answers["package_manager"]
    package_manager = getattr(package_managers, package_manager)()

    # Run tasks
    if answers["update_packages"]:
        package_manager.update_lists()
        package_manager.update_packages()
    if answers["install_packages"]:
        if not package_manager.lists_updated:
            package_manager.update_lists()
        package_manager.install(answers["install_packages"])
