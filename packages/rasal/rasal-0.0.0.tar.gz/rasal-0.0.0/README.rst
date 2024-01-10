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
.. |docs| image:: https://readthedocs.org/projects/rasal/badge/?style=flat
    :target: https://rasal.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/AidanJohnston/rasal/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/AidanJohnston/rasal/actions

.. |codecov| image:: https://codecov.io/gh/AidanJohnston/rasal/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/github/AidanJohnston/rasal

.. |version| image:: https://img.shields.io/pypi/v/rasal.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/rasal

.. |wheel| image:: https://img.shields.io/pypi/wheel/rasal.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/rasal

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/rasal.svg
    :alt: Supported versions
    :target: https://pypi.org/project/rasal

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/rasal.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/rasal

.. |commits-since| image:: https://img.shields.io/github/commits-since/AidanJohnston/rasal/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/AidanJohnston/rasal/compare/v0.0.0...main



.. end-badges

Resolution and Sensors and Lens.

* Free software: MIT license

Installation
============

::

    pip install rasal

You can also install the in-development version with::

    pip install https://github.com/AidanJohnston/rasal/archive/main.zip


Documentation
=============


https://rasal.readthedocs.io/


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
