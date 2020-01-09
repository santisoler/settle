"""
Define classes for using different package managers
"""
import subprocess
import platform

from .distros import DISTROS_PACKAGE_MANAGERS


def get_package_manager():
    """
    Get the package manager class suited for your Linux distribution

    Return
    ------
    package_manager : str
        Name of the package manager class that must be used on the
        current platform.
    """
    distribution = platform.dist()[0]
    distribution = distribution.lower()
    if distribution not in DISTROS_PACKAGE_MANAGERS:
        return None
    else:
        return DISTROS_PACKAGE_MANAGERS[distribution]


class BaseManager(object):
    """
    Base class for managing package managers

    This is not intended to be used directly, just to subclass it.
    """

    def __init__(self):
        self._lists_updated = False

    @property
    def lists_updated(self):
        return self._lists_updated

    def update_lists(self):
        commands = []
        if self.sudo:
            commands.append("sudo")
        commands.append(self.commands["update_lists"])
        self.run(commands)
        self._lists_updated = True

    def update_packages(self):
        commands = []
        if self.sudo:
            commands.append("sudo")
        commands.append(self.commands["update_packages"])
        self.run(commands)

    def install(self, packages):
        commands = []
        if self.sudo:
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

    def __init__(self, sudo=True):
        super().__init__()
        self.sudo = sudo
        self.commands = {
            "update_lists": "pacman -Sy",
            "update_packages": "pacman -Su",
            "install_packages": "pacman -S",
        }


class Apt(BaseManager):
    """
    Class to interact with apt package manager
    """

    def __init__(self, sudo=True):
        super().__init__()
        self.sudo = sudo
        self.commands = {
            "update_lists": "apt-get update",
            "update_packages": "apt-get upgrade",
            "install_packages": "apt-get install",
        }
