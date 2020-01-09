"""
Build and install the project.

Uses versioneer to manage version numbers using git tags.
"""
from setuptools import setup, find_packages

import versioneer


NAME = "settle"
FULLNAME = "Settle"
AUTHOR = "Santiago Soler"
AUTHOR_EMAIL = "santiago.r.soler@gmail.com"
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
LICENSE = "MIT License"
URL = "https://github.com/santisoler/settle"
DESCRIPTION = (
    "Settle your favorite packages on your fresh installed Linux distribution"
)
KEYWORDS = "linux post install packages script".split()
with open("README.md") as f:
    LONG_DESCRIPTION = "".join(f.readlines())
VERSION = versioneer.get_version()
CMDCLASS = versioneer.get_cmdclass()
CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: System Administrators",
    "Operating System :: POSIX",
    "Topic :: System",
    "Topic :: System :: Installation/Setup",
    "Topic :: Utilities",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "License :: OSI Approved :: {}".format(LICENSE),
]
PLATFORMS = "Any"
PACKAGES = find_packages(exclude=["doc"])
SCRIPTS = []
ENTRY_POINTS = {"console_scripts": "settle = settle.main:main"}
PACKAGE_DATA = {}
with open("requirements.txt") as f:
    INSTALL_REQUIRES = f.readlines()
PYTHON_REQUIRES = ">=3.6"

if __name__ == "__main__":
    setup(
        name=NAME,
        fullname=FULLNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        license=LICENSE,
        url=URL,
        platforms=PLATFORMS,
        entry_points=ENTRY_POINTS,
        scripts=SCRIPTS,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        install_requires=INSTALL_REQUIRES,
        python_requires=PYTHON_REQUIRES,
        cmdclass=CMDCLASS,
    )
