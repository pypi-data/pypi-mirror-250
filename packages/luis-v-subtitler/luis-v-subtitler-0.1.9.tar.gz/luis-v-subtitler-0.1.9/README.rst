========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-luis-v-subtitler/badge/?style=flat
    :target: https://python-luis-v-subtitler.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/LuisAVasquez/python-luis-v-subtitler/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/LuisAVasquez/python-luis-v-subtitler/actions

.. |codecov| image:: https://codecov.io/gh/LuisAVasquez/python-luis-v-subtitler/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/github/LuisAVasquez/python-luis-v-subtitler

.. |version| image:: https://img.shields.io/pypi/v/luis-v-subtitler.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/luis-v-subtitler

.. |wheel| image:: https://img.shields.io/pypi/wheel/luis-v-subtitler.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/luis-v-subtitler

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/luis-v-subtitler.svg
    :alt: Supported versions
    :target: https://pypi.org/project/luis-v-subtitler

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/luis-v-subtitler.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/luis-v-subtitler

.. |commits-since| image:: https://img.shields.io/github/commits-since/LuisAVasquez/python-luis-v-subtitler/v0.1.9.svg
    :alt: Commits since latest release
    :target: https://github.com/LuisAVasquez/python-luis-v-subtitler/compare/v0.1.9...main



.. end-badges

A Python package to use AI to subtitle any video in any language

* Free software: MIT license

Installation
============

::

    pip install luis-v-subtitler

You can also install the in-development version with::

    pip install https://github.com/LuisAVasquez/python-luis-v-subtitler/archive/main.zip


Documentation
=============


https://python-luis-v-subtitler.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
