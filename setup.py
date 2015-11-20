#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

import podpublish as pkg
from setuptools import setup, find_packages
from requirements import RequirementsParser
requirements = RequirementsParser()

setup(
    name=pkg.__packagename__,
    version=pkg.__version__,
    author=pkg.__author__,
    author_email=pkg.__author_email__,
    maintainer=pkg.__maintainer__,
    maintainer_email=pkg.__maintainer_email__,
    url=pkg.__url__,
    description=pkg.__description__,
    long_description=open('README.md').read() + open('CHANGES').read() +
    open('TODO').read() + open('AUTHORS').read(),
    download_url=pkg.__download_url__,
    classifiers=pkg.__classifiers__,
    platforms=pkg.__platforms__,
    license=pkg.__license__,
    keywords=pkg.__keywords__,
    #packages=find_packages(exclude=['lextab.*', 'parsetab.*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements.install_requires,
    setup_requires=requirements.setup_requires,
    tests_require=requirements.tests_require,
    extras_require=requirements.extras_require,
    dependency_links=requirements.dependency_links,
    test_suite='nose.collector',
)

################################################################################
# vim:et:ft=python:nowrap:sts=4:sw=4:ts=4
