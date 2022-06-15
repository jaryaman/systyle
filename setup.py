#!/usr/bin/env python3


import sys
from setuptools import find_packages
from setuptools import setup

requirements = [
    'matplotlib',
    'jupyter',
    'pandas',
    'numpy',
    'scipy',
    'seaborn',
    'pyyaml',
]

if '__main__' == __name__:
    setup(
        author='Juvid Aryaman',
        author_email='j.aryaman25@gmail.com',
        packages=find_packages(),
        license=open('LICENSE.txt').read(),
        long_description=open('README.md').read(),
        name=open('modulename.txt').read().replace('\n', ''),
        version=open('version.txt').read().strip(),
        include_package_data=True,
        install_requires = requirements,
    )

sys.exit(0)
