#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 13:22:07 2023

@author: wenkangng
"""

from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.1.2'
DESCRIPTION = 'Read the financial statement of listed company'

# Setting up
setup(
    name="financial_statement",
    version=VERSION,
    author="Ng wen kang",
    author_email="kangwen177@gmail.com",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests', 'numpy', 'bs4', 'pandas', 'datetime'],
    keywords=['python', 'finance', 'financial statement', 'stock market'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

