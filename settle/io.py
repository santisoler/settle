"""
Functions to read and save files
"""
import yaml
from .utils import check_valid_default_packages


def read_packages_yaml(packages_yaml):
    """
    Read packages YAML file
    """
    packages = yaml.load(packages_yaml, Loader=yaml.FullLoader)
    # Pop default packages if any
    default_packages = []
    if "default" in packages:
        default_packages = packages.pop("default")
        check_valid_default_packages(packages, default_packages)
    return packages, default_packages
