# -*- coding: utf-8 -*-
import ast
import re

from pip.req import parse_requirements
from setuptools import setup, find_packages

# get version from __version__ variable in gps_tracking_management/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('gps_tracking_management/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

requirements = parse_requirements("requirements.txt", session="")

setup(
    name='gps_tracking_management',
    version=version,
    description='Application for Managing HPS Tracking Activities',
    author=' Bituls Company Limited',
    author_email='info@bituls.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[str(ir.req) for ir in requirements],
    dependency_links=[str(ir._link) for ir in requirements if ir._link]
)
