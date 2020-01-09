"""
Utils functions for Settle
"""


def check_valid_default_packages(packages, default):
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
