#!/usr/bin/env python
import os
from setuptools import setup, find_packages

dependencies = [
    'beautifulsoup4>=4.0.2',
    'lxml>=2.3.2',
    'requests>=2.2.1',
]


setup(
    name='wmrevolution',
    version='0.1',
    description='various modules to get wm course info',
    author='Ryan Beatty',
    author_email='rvbeatty@email.wm.edu',
    url='https://github.com/RyanBeatty/wmrevolution',
    install_requires=dependencies,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'W&M :: Scrapping :: Worl-Domination',
    ],
    test_suite="tests",
)
