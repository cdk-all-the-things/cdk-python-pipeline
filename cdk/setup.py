#!/usr/bin/env python
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

setup(
    name='cdk_python_pipeline-cdk',
    version='1.0',
    description='CDK code for deploying the serverless service',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.10.6',
    ],
    url='https://github.com/cdk-all-the-things/cookiecutter-cdk-python',
    author='Wilford Brimley',
    author_email='wilford@brimley.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_data={'': ['*.json']},
    include_package_data=True,
    python_requires='>=3.10.6',
    install_requires=[],
)
