"""
Define classes for using different package managers
"""
import os
import subprocess
import distro

# Define dictionary matching linux distro to package manager classname
# defined in settle/package_managers.py
DISTROS_PACKAGE_MANAGERS = {
    "manjaro linux": "pacman",
    "arch": "pacman",
    "ubuntu": "apt",
    "debian": "apt",
}

# Define list of supported package managers
PACKAGE_MANAGERS = ["apt", "pacman", "yay"]

# Dictionary with package managers and corresponding classes
PACKAGE_MANAGERS_CLASSES = {p: p.title() for p in PACKAGE_MANAGERS}


def get_package_manager(package_manager=None):
    """
    Get the package manager class that will manage the installations

    Parameters
    ----------
    package_manager: str (optional)
        Package manager name. If None, the better suited package manager will be chosen
        based on the distro.

    Returns
    -------
    package_manager_classname: str
        Name of the package manager class.
    """
    if package_manager is None:
        package_manager = guess_package_manager()
    else:
        if package_manager not in PACKAGE_MANAGERS:
            raise ValueError("Invalid package manager '{}'".format(package_manager))
    return PACKAGE_MANAGERS_CLASSES[package_manager]


def guess_package_manager():
    """
    Guess which package manager class is suited for your Linux distribution

    Return
    ------
    package_manager : str
        Name of the package manager
    """
    distribution = distro.linux_distribution()[0]
    distribution = distribution.lower()
    if distribution not in DISTROS_PACKAGE_MANAGERS:
        raise ValueError(
            "Couldn't choose a package manager for your distro. "
            + "This may be caused because your distro is not supported or "
            + "Settle cannot identify it properly. "
            + "Try specifying the package manager you want to use through the "
            + "--package-manager option."
        )
    return DISTROS_PACKAGE_MANAGERS[distribution]


class BaseManager(object):
    """
    Base class for managing package managers

    This is not intended to be used directly, just to subclass it.
    In order to subclass it, override the class attributes `needs_sudo` and `commands`
    according to the package manager specific needs.
    """

    # Specify if the package manager should be ran with sudo privileges
    needs_sudo = False
    # Specify how update lists, update packages and install packages
    # with the package manager.
    commands = {
        "update_lists": None,
        "update_packages": None,
        "install_packages": None,
    }

    def __init__(self):
        self._lists_updated = False

    @property
    def lists_updated(self):
        return self._lists_updated

    @property
    def sudo(self):
        "Check if we have sudo privileges"
        return os.getuid() != 0

    def update_lists(self):
        "Update package lists"
        commands = []
        if self.needs_sudo and self.sudo:
            commands.append("sudo")
        commands.append(self.commands["update_lists"])
        self.run(commands)
        self._lists_updated = True

    def update_packages(self):
        "Update packages"
        commands = []
        if self.needs_sudo and self.sudo:
            commands.append("sudo")
        commands.append(self.commands["update_packages"])
        self.run(commands)

    def install(self, packages):
        "Install packages"
        commands = []
        if self.needs_sudo and self.sudo:
            commands.append("sudo")
        commands.append(self.commands["install_packages"])
        commands += packages
        self.run(commands)

    def run(self, commands):
        subprocess.run(" ".join(commands), shell=True)


class Pacman(BaseManager):
    """
    Class to interact with pacman package manager
    """

    needs_sudo = True
    commands = {
        "update_lists": "pacman -Sy",
        "update_packages": "pacman -Su",
        "install_packages": "pacman -S",
    }


class Apt(BaseManager):
    """
    Class to interact with apt package manager
    """

    needs_sudo = True
    commands = {
        "update_lists": "apt-get update",
        "update_packages": "apt-get upgrade",
        "install_packages": "apt-get install",
    }


class Yay(BaseManager):
    """
    Class to interact with the yay package manager
    """

    needs_sudo = False
    commands = {
        "update_lists": "yay -Sy",
        "update_packages": "yay -Su",
        "install_packages": "yay -S",
    }
