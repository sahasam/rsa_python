#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='rsapy',
    version='1.0',
    description='Python RSA encryption implementation in python',
    author='Sahas Munamala',
    author_email='gward@python.net',
    url='https://github.com/sahasam/rsa_python',
    license='MIT License',
    packages=find_packages(),
    entry_points={"console_scripts": ["rsapy=rsapy.__main__:main"]},
)
