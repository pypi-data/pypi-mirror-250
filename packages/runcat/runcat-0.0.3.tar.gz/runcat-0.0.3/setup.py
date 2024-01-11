# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from runcat import __version__, __description__

try:
    long_description = open(os.path.join('runcat', "README.md"), encoding='utf-8').read()
except IOError:
    long_description = ""

setup(
    name="runcat",
    version=__version__,
    description=__description__,
    author="杨康",
    author_email="772840356@qq.com",
    url="https://gitee.com/bluepang2021/runcat",
    platforms="PC",
    packages=find_packages(),
    long_description=long_description,
    python_requires='>=3.9',
    classifiers=[
        "Programming Language :: Python :: 3.9"
    ],
    install_requires=[
        'pandas==1.3.4',
        'openpyxl==3.0.9',
        'pycryptodome==3.14.1',
        'PyMySQL==0.10.1',
        'requests==2.31.0'
    ]
)
