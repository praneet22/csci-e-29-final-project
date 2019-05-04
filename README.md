Overview
========  

| Branch | Build Status |
| ------ | :-------- | 
| Master | [![Build Status](https://travis-ci.com/praneetmsft/csci-e-29-final-project.svg?branch=master)](https://travis-ci.com/praneetmsft/csci-e-29-final-project) | 
| Develop | [![Build Status](https://travis-ci.com/praneetmsft/csci-e-29-final-project.svg?branch=develop)](https://travis-ci.com/praneetmsft/csci-e-29-final-project) |
| docs | [![Documentation Status](https://readthedocs.org/projects/2019sp-final-project-praneetmsft/badge/?style=flat)](https://readthedocs.org/projects/2019sp-final-project-praneetmsft)  |
| tests | [![Travis-CI Build Status](https://travis-ci.org/csci-e-29/2019sp-final-project-praneetmsft.svg?branch=master)](https://travis-ci.org/csci-e-29/2019sp-final-project-praneetmsft)  [![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/github/csci-e-29/2019sp-final-project-praneetmsft?branch=master&svg=true)](https://ci.appveyor.com/project/csci-e-29/2019sp-final-project-praneetmsft) |
| package | [![PyPI Package latest release](https://img.shields.io/pypi/v/final-project.svg)](https://pypi.org/project/final-project) [![PyPI Wheel](https://img.shields.io/pypi/wheel/final-project.svg)](https://pypi.org/project/final-project) [![Supported versions](https://img.shields.io/pypi/pyversions/final-project.svg)](https://pypi.org/project/final-project) [![Supported implementations](https://img.shields.io/pypi/implementation/final-project.svg)](https://pypi.org/project/final-project)  [![Commits since latest release](https://img.shields.io/github/commits-since/csci-e-29/2019sp-final-project-praneetmsft/v0.0.0.svg)](https://github.com/csci-e-29/2019sp-final-project-praneetmsft/compare/v0.0.0...master)  |


-   Free software: BSD 2-Clause License

Installation
------------

    pip install final-project

Documentation
-------------

<https://2019sp-final-project-praneetmsft.readthedocs.io/>

Development
-----------

To run the all tests run:

    tox

Note, to combine the coverage data from all the tox environments run:

+------+---------------------------------------------------------------+
| Wind |     set PYTEST_ADDOPTS=--cov-append                           |
| ows  |     tox                                                       |
+------+---------------------------------------------------------------+
| Othe |     PYTEST_ADDOPTS=--cov-append tox                           |
| r    |                                                               |
+------+---------------------------------------------------------------+
