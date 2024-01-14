from setuptools import setup
import os
from setuptools import setup

with open('requirements.txt') as f:
    requirements_txt = f.read().splitlines()

setup(
    name='latio',
    version='v0.0.2',
    url='https://github.com/latiotech/LAST',
    license='GPL-3.0 license',
    author='James Berthoty',
    author_email='james@latio.tech',
    description='Latio Application Security Tester - Uses OpenAPI to scan for security issues in code changes',
    install_requires=requirements_txt,
    entry_points = {
            'console_scripts': ['LAST = LAST:main'],
        },

)
