#!/usr/bin/env python
"""
EmeraldTree, a light-weight toolkit for XML processing in Python
================================================================

EmeraldTree is a fork of ElementTree - the main differences are:

* It has a slightly different API:

  - Handling of text: it uses unicode objects as children (not as
    "tail" attributes of the elements)

* API cleanups, removing backward compatibility 

* Better unicode support

* PolyglotWriter (for writing html5 that is also well-formed xml)

* Other improvements / optimizations

The fork happened at ElementTree 1.3a3-20070912-preview.

For more details please see the `EmeraldTree repository <http://hg.moinmo.in/EmeraldTree/>`_.

"""

from setuptools import setup

DESCRIPTION="EmeraldTree - a light-weight XML object model for Python."

setup(
    name="emeraldtree",
    version="0.10.0",
    url='http://hg.moinmo.in/EmeraldTree/',
    author="Bastian Blank",
    author_email="bblank@thinkmo.de",
    keywords=["xml", "html", "html5", "polyglot", "element", "tree", "dom", "unicode", ],
    description=DESCRIPTION,
    long_description=__doc__,
    license="Python (MIT style)",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'License :: OSI Approved :: Python Software Foundation License',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
    ],
    packages=["emeraldtree"],
    install_requires=['six>=1.3.0'],
    platforms="any",
)

