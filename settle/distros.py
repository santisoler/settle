"""
Dictionaries matching distributions and package managers
"""
# Define dictionary matching linux distro to package manager classname
# defined in settle/package_managers.py
DISTROS_PACKAGE_MANAGERS = {
    "arch": "Pacman",
    "ubuntu": "Apt",
    "debian": "Apt",
}

# Define list of package managers
PACKAGE_MANAGERS = list(set(DISTROS_PACKAGE_MANAGERS.values()))
