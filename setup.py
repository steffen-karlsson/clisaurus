#!/usr/bin/env python

from setuptools import find_packages
from distutils.core import setup

import clisaurus

install_requires = [
    'requests>=2.4.3',
    'colorama>=0.3.2',
    'argparse>=1.2.0',
    'beautifulsoup4>=4.4.0',
    'tabulate>=0.7.5'
]

setup(
    name='clisaurus',
    version=clisaurus.__version__,
    description=clisaurus.__doc__.strip(),
    url='https://github.com/steffenkarlsson/clisaurus/',
    download_url='https://github.com/steffenkarlsson/clisaurus/',
    author=clisaurus.__author__,
    author_email='steffen.karlsson@gmail.com',
    license=clisaurus.__licence__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'http = clisaurus.__main__:main',
        ],
    },
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
)