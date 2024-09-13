#!/usr/bin/env python3
from __future__ import absolute_import, print_function

# Standard Library
import io
import os
import re
from glob import glob
from os.path import basename, dirname, join, splitext

# Third Party Libraries
from setuptools import find_packages, setup


if os.environ.get('CIRCLECI', None) is not None:
    # monkey-patch distutils upload
    #
    # http://bugs.python.org/issue21722
    try:
        from distutils.command import upload as old_upload_module
        from ci.upload import upload as fixed_upload

        old_upload_module.upload = fixed_upload
    except ImportError:
        # In some cases I install elmo-w3af-api-client in CircleCI, but not from the
        # repository where the ci module is present
        pass


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


def requires(filename):
    """Returns a list of all pip requirements
    :param filename: the Pip requirement file (usually 'requirements.txt')
    :return: list of modules
    :rtype: list
    """
    modules = []
    with open(filename, 'r') as pipreq:
        for line in pipreq:
            line = line.strip()
            # Checks if line starts with a comment or referencing
            # external pip requirements file (with '-e'):
            if line.startswith('#') or line.startswith('-') or not line:
                continue
            modules.append(line)
    return modules


setup(
    name='elmo-w3af-api-client',

    license='GNU General Public License v2 (GPLv2)',
    platforms='Linux',

    description='REST API client to consume w3af',
    long_description=read('README.rst'),

    author='Andres Riancho',
    author_email='andres.riancho@gmail.com',
    url='https://github.com/andresriancho/elmo-w3af-api-client/',

    packages=find_packages(),
    py_modules=["w3af_api_client"],
    include_package_data=True,
    install_requires=[
        "future==0.18.2",
        "requests==2.22.0",
        "six==1.13.0",
        "setuptools",
        "urllib3"
    ],

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Monitoring'
    ],

    # In order to run this command: python setup.py test
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', 'pytest-cov', 'pytest-catchlog'],
)
