Change Log
==========

Version 0.11.0 (2024-04-05)
---------------------------

Fixes:

- html parser: fix extraction of encoding from meta element
- use raw string for regex, fixes "DeprecationWarning: invalid escape
  sequence \s" and others.

New features:

- include version infos into emeraldtree.__init__

Other changes:

- packaging modernized / enhanced: pyproject.toml, MANIFEST.in, setuptools-scm
- requires Python >= 3.9 now (dropped Python 2.x, removed "six")
- add github actions CI, remove travis CI config
- rst markup fixes / clean ups
- use tox for testing

Version 0.10.0 (2015-06-10)
---------------------------

Fixes:

- fix setup.py - platform and no download_url
- invalid output from HTML converter parsing preformatted code, multiline
  paragraphs: part 2 of 2 fixes moin2 #516

Other changes:

- ported to Python 2.7 / >= 3.3 using six

Version 0.9.0 (2011-01-22)
--------------------------

First release on PyPI.

