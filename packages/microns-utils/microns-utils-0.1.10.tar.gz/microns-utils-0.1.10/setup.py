#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'microns_utils', 'version.py')) as f:
    exec(f.read())

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().split()

setup(
    name='microns-utils',
    version=__version__,
    description='utilities for MICrONS',
    author='Stelios Papadopoulos, Christos Papadopoulos',
    author_email='spapadop@bcm.edu, cpapadop@bcm.edu',
    packages=find_packages(exclude=[]),
    install_requires=requirements
)