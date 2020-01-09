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
    return parser
