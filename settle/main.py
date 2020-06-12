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
from .argparser import create_argparser
from .questions import Asker
from .io import read_packages_yaml


def main():
    # Parse command line arguments
    parser = create_argparser()
    arguments = parser.parse_args()

    # Read packages.yml and get defaults
    packages_dict, default_categories = read_packages_yaml(arguments.packages)

    # Get package manager instance
    package_manager = get_package_manager(arguments.package_manager)
    package_manager = getattr(package_managers, package_manager)()

    # Ask questions
    asker = Asker(
        packages_dict, default_categories, list_packages=arguments.list_packages,
    )
    answers = asker.ask_questions()

    # Continue only if the last confirmation question is true
    if not answers["continue"]:
        sys.exit()

    # Run tasks
    if answers["update_packages"]:
        package_manager.update_lists()
        package_manager.update_packages()
    if answers["install_packages"]:
        if not package_manager.lists_updated:
            package_manager.update_lists()
        package_manager.install(answers["install_packages"])
