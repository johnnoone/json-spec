#!/usr/bin/env python

import versioneer
from setuptools import setup, find_packages

setup(
    name='json-spec',
    version=versioneer.get_version(),
    description='Implements JSON Schema, JSON Pointer and JSON Reference.',
    author='Xavier Barbosa',
    author_email='clint.northwood@gmail.com',
    license='BSD',
    url='http://github.com/johnnoone/json-spec',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    keywords=[
        'json',
        'utilitaries',
        'validation',
        'json-pointer',
        'json-reference',
        'json-schema'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: OpenStack',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        'six',
    ],
    extras_require={
        'ip': [],
        'ip:python_version=="2.7"': ['ipaddress'],
        'ip:python_version=="3.2"': ['ipaddress'],
        'cli': ['termcolor']
    },
    entry_points={
        'console_scripts': [
            'json = jsonspec.cli:main',
        ],
        'jsonspec.cli.commands': [
            'validate = jsonspec.cli:ValidateCommand',
            'extract = jsonspec.cli:ExtractCommand',
            'add = jsonspec.cli:AddCommand',
            'remove = jsonspec.cli:RemoveCommand',
            'replace = jsonspec.cli:ReplaceCommand',
            'move = jsonspec.cli:MoveCommand',
            'copy = jsonspec.cli:CopyCommand',
            'check = jsonspec.cli:CheckCommand',
        ],
        'jsonspec.reference.contributions': [
            'spec = jsonspec.reference.providers:SpecProvider',
        ],
        'jsonspec.validators.formats': [
            'email = jsonspec.validators.util:validate_email',
            'hostname = jsonspec.validators.util:validate_hostname',
            'ipv4 = jsonspec.validators.util:validate_ipv4 [ip]',
            'ipv6 = jsonspec.validators.util:validate_ipv6 [ip]',
            'regex = jsonspec.validators.util:validate_regex',
            'uri = jsonspec.validators.util:validate_uri',
            'css.color = jsonspec.validators.util:validate_css_color',
            'rfc3339.datetime = jsonspec.validators.util:validate_rfc3339_datetime',
            'utc.datetime = jsonspec.validators.util:validate_utc_datetime',
            'utc.date = jsonspec.validators.util:validate_utc_date',
            'utc.time = jsonspec.validators.util:validate_utc_time',
            'utc.millisec = jsonspec.validators.util:validate_utc_millisec',
        ]
    },
    cmdclass=versioneer.get_cmdclass()
)
