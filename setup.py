#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = \
'''Read a bibtex file and generate a graph of co-authorship'''


setup(
    name='coauthgraph',
    version='0.1.0.0',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['coauthgraph'],
    package_dir={'coauthgraph': 'coauthgraph'},
    entry_points={
        'console_scripts': ['coauthgraph = coauthgraph.coauthgraph:main']
    },
    url='https://github.com/bjpop/coauthgraph',
    license='LICENSE',
    description=('Read a bibtex file and generate a graph of co-authorship'),
    long_description=(LONG_DESCRIPTION),
    install_requires=["bibtexparser"],
)
