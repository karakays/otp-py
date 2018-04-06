#!/usr/bin/python
# -*- coding: utf-8
from setuptools import setup, find_packages

setup(
    name='otp',
    version='0.1.0.dev1',
    author='Selçuk Karakayalı',
    author_email='skarakayali@gmail.com',
    maintainer='Selçuk Karakayalı',
    url='http://github.com/karakays/otp-py/',
    packages=find_packages(),
    python_requires='>=3',
    license='MIT',
    keywords=['otp', 'otp-codes', 'otp-generator', 'authenticator'],
    description='Generate one time passwords',
    long_description=open('README.rst').read(),
    scripts=['bin/otp']
)
