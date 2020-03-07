"""
Create argument parser for Settle
"""
import argparse


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
        "--dry-run",
        action="store_true",
        help="perform a trial run, but no changes will be made",
    )
    return parser
