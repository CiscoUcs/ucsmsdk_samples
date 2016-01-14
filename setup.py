#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "ucsmsdk"
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='ucsmsdk_samples',
    version='0.1.0',
    description="samples for ucsmsdk",
    long_description=readme + '\n\n' + history,
    author="Vikrant Balyan",
    author_email='vvb@cisco.com',
    url='https://github.com/vijayvikrant/ucsmsdk_samples',
    packages=[
        'ucsmsdk_samples',
    ],
    package_dir={'ucsmsdk_samples':
                 'ucsmsdk_samples'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='ucsmsdk_samples',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
