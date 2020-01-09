"""
Main function for running Settle
"""
import os
import subprocess
import yaml
import inquirer
import platform
from inquirer.themes import load_theme_from_dict

from . import package_managers
from .package_managers import get_package_manager
from .distros import DISTROS_PACKAGE_MANAGERS, PACKAGE_MANAGERS
from .argparser import create_argparser
from .utils import check_valid_default
from .inquirer_theme import inquirer_theme


def main():
    # Define empty list for questions
    questions = []

    # Parse command line arguments
    parser = create_argparser()
    arguments = parser.parse_args()

    # Read packages.yml and get defaults
    packages = yaml.load(arguments.packages, Loader=yaml.FullLoader)
    default = []
    if "default" in packages:
        default = packages.pop("default")
        check_valid_default(packages, default)

    # Get package manager class
    package_manager = get_package_manager()
    if package_manager is None:
        questions.append(
            inquirer.List(
                "package_manager",
                message="What package manager should we use?",
                choices=PACKAGE_MANAGERS,
            )
        )

    # Ask questions and get answers
    questions += [
        inquirer.Confirm(
            "update_packages",
            message="Do you want to update all packages?",
            default=True,
        ),
        inquirer.Checkbox(
            "install_packages",
            message="What packages do you want to install?",
            choices=list(packages.keys()),
            default=default,
        ),
        inquirer.Confirm(
            "run_tasks",
            message="Do you really want to perform the chosen tasks?",
            default=True,
        ),
    ]
    answers = inquirer.prompt(questions, theme=load_theme_from_dict(inquirer_theme))

    # Continue only if the last confirmation question is true
    if answers["run_tasks"]:

        # Initialize package manager
        if "package_manager" in answers:
            package_manager = answers["package_manager"]
        package_manager = getattr(package_managers, package_manager)()

        # Run tasks
        if answers["update_packages"]:
            package_manager.update_lists()
            package_manager.update_packages()
        if answers["install_packages"]:
            chosen_packages = []
            for group in answers["install_packages"]:
                chosen_packages += packages[group]
            if not package_manager.lists_updated:
                package_manager.update_lists()
            package_manager.install(chosen_packages)
