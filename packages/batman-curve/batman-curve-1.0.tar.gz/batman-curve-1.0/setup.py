#!/usr/bin/env python
# coding=utf-8

import os
import sys

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)

import versioneer  # noqa: E402

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="batman-curve",
    description="A Python library for generating the iconic Batman curve.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avitase/batman-curve",
    author="Nis Meinert",
    author_email="mail@nismeinert.de",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.10",
    install_requires=[
        "numpy",
    ],
    extras_require={
        "dev": [
            "pre-commit",
            "pytest",
            "pytest-cov",
            "matplotlib",
        ],
    },
)
