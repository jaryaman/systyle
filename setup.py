#!/usr/bin/env python3


import sys
from setuptools import find_packages
from setuptools import setup

# *** main ***

if '__main__' == __name__:
    setup(
        author='Juvid Aryaman',
        author_email='j.aryaman25@gmail.com',
        packages=find_packages(),
        license=open('LICENSE.txt').read(),
        long_description=open('README.md').read(),
        version=open('version.txt').read().strip(),
    )

sys.exit(0)
