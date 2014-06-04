#!/usr/bin/env python

# http://alexis.notmyidea.org/distutils2/setupcfg.html

from setuptools import setup, find_packages

setup(
    setup_requires=['pbr'],
    pbr=True,
    namespace_packages=['json'],
    packages=find_packages('src'),
    package_dir = {'': 'src'},
)