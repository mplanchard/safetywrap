# -*- coding: utf-8 -*-
"""Setup file for the skelethon."""

import typing as t
from os.path import dirname, exists, join, realpath
from setuptools import setup, find_packages

cwd = dirname(realpath(__file__))

########################################################################
# Contact Information
########################################################################

URL = "https://www.github.com/mplanchard/safetywrap"
AUTHOR = "Matthew Planchard"
EMAIL = "msplanchard@gmail.com"


########################################################################
# Package Description
########################################################################

NAME = "safetywrap"
SHORT_DESC = "Rust-inspired typesafe result types"

with open(join(cwd, "README.md")) as readme:
    LONG_DESC = readme.read()
LONG_DESC_CONTENT_TYPE = "text/markdown"

KEYWORDS = [
    "python",
    "rust",
    "result",
    "option",
    "typed",
    "types",
    "typesafe",
    "monad",
    "wrapper",
    "safety",
]
CLASSIFIERS = [
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers for all
    # available setup classifiers
    # "Development Status :: 1 - Planning",
    # 'Development Status :: 2 - Pre-Alpha',
    # "Development Status :: 3 - Alpha",
    "Development Status :: 4 - Beta",
    # 'Development Status :: 5 - Production/Stable',
    # 'Development Status :: 6 - Mature',
    # 'Framework :: AsyncIO',
    # 'Framework :: Flask',
    # 'Framework :: Sphinx',
    # 'Environment :: Web Environment',
    "Intended Audience :: Developers",
    # 'Intended Audience :: End Users/Desktop',
    # 'Intended Audience :: Science/Research',
    # 'Intended Audience :: System Administrators',
    # 'License :: Other/Proprietary License',
    # 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    # 'License :: OSI Approved :: MIT License',
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    # 'Programming Language :: Python :: Implementation :: PyPy',
]


########################################################################
# Dependency Specification
########################################################################

PYTHON_REQUIRES = ">=3.6"
PACKAGE_DEPENDENCIES: t.Tuple[str, ...] = ()
SETUP_DEPENDENCIES: t.Tuple[str, ...] = ()
TEST_DEPENDENCIES: t.Tuple[str, ...] = ()
EXTRAS_DEPENDENCIES: t.Dict[str, t.Sequence[str]] = {
    "dev": (
        TEST_DEPENDENCIES
        + (
            "black",
            "coverage",
            "flake8",
            "ipdb",
            "ipython",
            "mypy",
            "pydocstyle",
            "pylint",
            "pytest",
            "pytest-cov",
            "tox",
            "twine",
            "typeguard",
            "wheel",
        )
    )
}


########################################################################
# Package Extras
########################################################################

ENTRY_POINTS: t.Union[str, t.Dict[str, t.Union[str, t.Sequence[str]]]] = {}
PACKAGE_DATA: t.Dict[str, t.Sequence[str]] = {"safetywrap": ["py.typed"]}


########################################################################
# Setup Logic
########################################################################

PACKAGE_DIR = realpath(dirname(__file__))


REQ_FILE = join(PACKAGE_DIR, "requirements_unfrozen.txt")
if exists(REQ_FILE):
    with open(join(PACKAGE_DIR, "requirements.txt")) as reqfile:
        for ln in (l.strip() for l in reqfile):
            if ln and not ln.startswith("#"):
                PACKAGE_DEPENDENCIES += (ln,)


__version__ = "0.0.0"

with open(join(cwd, "src/{}/__init__.py".format(NAME))) as init_file:
    for line in init_file:
        # This will set __version__ and __version_info__ variables locally
        if line.startswith("__version"):
            exec(line)

setup(
    author_email=EMAIL,
    author=AUTHOR,
    classifiers=CLASSIFIERS,
    description=SHORT_DESC,
    entry_points=ENTRY_POINTS,
    extras_require=EXTRAS_DEPENDENCIES,
    keywords=KEYWORDS,
    long_description_content_type=LONG_DESC_CONTENT_TYPE,
    long_description=LONG_DESC,
    name=NAME,
    package_data=PACKAGE_DATA,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=PYTHON_REQUIRES,
    setup_requires=SETUP_DEPENDENCIES,
    tests_require=TEST_DEPENDENCIES,
    url=URL,
    version=__version__,
)
