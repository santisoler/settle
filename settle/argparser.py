"""
Create argument parser for Settle
"""
import argparse

from .package_managers import PACKAGE_MANAGERS


DESCRIPTION = "Settle your favorite packages on your fresh installed Linux distribution"
PACKAGES_HELP_LINE = "YAML file containing packages names."


def create_argparser():
    """
    Create argparser for Settle
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "packages",
        metavar="packages.yml",
        type=argparse.FileType("r"),
        help=PACKAGES_HELP_LINE,
        default="",
    )
    parser.add_argument(
        "--list-packages",
        "-l",
        action="store_true",
        help="list all packages inside packages.yml instead of showing categories",
    )
    parser.add_argument(
        "-p",
        "--package-manager",
        type=str,
        help=(
            "which package manager to use. If no package manager is specified, "
            + "Settle will guess which one to use based on your distro. "
            + "The supported package managers are: "
            + "{}.".format(", ".join(PACKAGE_MANAGERS))
        ),
    )
    return parser
