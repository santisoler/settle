"""
Function for reading packages YAML file
"""
import yaml


def read_packages_yaml(packages_yaml):
    """
    Read packages YAML file
    """
    packages = yaml.load(packages_yaml, Loader=yaml.FullLoader)
    # Pop default packages if any
    default_packages = []
    if "default" in packages:
        default_packages = packages.pop("default")
        _check_valid_default_packages(packages, default_packages)
    return packages, default_packages


def _check_valid_default_packages(packages, default):
    "Check if the groups in default are valid"
    missing_groups = [group for group in default if group not in packages]
    if missing_groups:
        if len(missing_groups) == 1:
            plural = ""
            missing_groups = missing_groups[0]
        else:
            plural = "s"
            missing_groups = "', '".join(missing_groups)
        raise ValueError(
            "Group{0} '{1}' not recognized as valid package group{0}".format(
                plural, missing_groups
            )
            + " inside the passed YAML package file."
        )
