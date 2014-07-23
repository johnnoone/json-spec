#!/usr/bin/env python

from setuptools import setup

setup(
    setup_requires=['pbr'],
    extras_require={
        'ip': [],
        'ip:python_version=="2.7"': ['ipaddress'],
        'ip:python_version=="3.2"': ['ipaddress'],
        'cli': ['termcolor']
    },
    pbr=True,
)
