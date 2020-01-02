"""
Main function for running Settle
"""
import os
import subprocess
import yaml
import inquirer

from .argparser import create_argparser
from .utils import check_valid_default
from .package_managers import get_package_manager, PACKAGE_MANAGERS


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
    package_manager = package_manager()
    if package_manager is None:
        questions.append(
            inquirer.List(
                "package_manager",
                message="What package manager should we use?",
                choices=PACKAGE_MANAGERS,
            )
        )

    # Ask questions
    questions += [
        inquirer.Confirm(
            "update_lists",
            message="Do you want to refresh repositories databases?",
            default=True,
        ),
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
    ]
    answers = inquirer.prompt(questions)
    print(answers)

    # Run tasks
    if answers["update_packages"]:
        package_manager.update_lists()
        package_manager.update_packages()
    if answers["update_lists"] and not answers["update_packages"]:
        package_manager.update_lists()
    if answers["install_packages"]:
        chosen_packages = []
        for group in answers["install_packages"]:
            chosen_packages += packages[group]
        if not package_manager.lists_updated:
            package_manager.update_lists()
        package_manager.install(chosen_packages)
