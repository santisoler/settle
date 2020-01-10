"""
Function for reading packages YAML file
"""
import yaml


def read_packages_yaml(packages_yaml):
    """
    Read packages YAML file
    """
    packages = yaml.load(packages_yaml, Loader=yaml.FullLoader)
    # Pop default categories if any
    default_categories = []
    if "default" in packages:
        default_categories = packages.pop("default")
        _check_valir_default_categories(packages, default_categories)
    return packages, default_categories


def _check_valir_default_categories(packages, default):
    "Check if the categories in default are valid"
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
