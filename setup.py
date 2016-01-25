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
    license="http://www.apache.org/licenses/LICENSE-2.0",
    zip_safe=False,
    keywords='ucsmsdk_samples',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    extras_require={
        'docs': ['sphinx<1.3', 'sphinxcontrib-napoleon',
                 'sphinx_rtd_theme'],
    }
)
