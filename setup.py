#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='pytest-htmllint',
    packages=find_packages(),
    version='0.0.1',


    entry_points={
        'pytest11': ['name_of_plugin = htmllint.lint']
    },

    author='Joe Alcorn',
    author_email='joealcorn123@gmail.com',
    description='HTML style checking as a py.test plugin',
    license='MIT',
    url='https://github.com/buttscicles/pytest-htmllint'
)
