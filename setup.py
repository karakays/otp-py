#!/usr/bin/python
# -*- coding: utf-8
from setuptools import setup, find_packages

pkg_vars = {}

with open("otp/_version.py") as fp:
    exec(fp.read(), pkg_vars)

setup(
    name='otp-py',
    version=pkg_vars['__version__'],
    author='Selçuk Karakayalı',
    author_email='skarakayali@gmail.com',
    maintainer='Selçuk Karakayalı',
    url='http://github.com/karakays/otp-py/',
    packages=find_packages(),
    install_requires=['pyqrcode>=1.2.1'],
    python_requires='>=3.6',
    license='MIT',
    keywords=['otp', 'otp-codes', 'otp-generator', 'authenticator'],
    description='Generate one time passwords',
    long_description=open('README.rst').read(),
    scripts=['bin/otp'],
    classifiers=[ "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License"]
)
