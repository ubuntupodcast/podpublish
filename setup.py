#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

import podpublish as pkg
from setuptools import setup, find_packages


def get_requirements(fname):
    try:
        with open(fname, 'r') as fh:
            requirements = [l.strip() for l in fh]
    except:
        requirements = []

    return requirements


def get_extras(fname):
    extras = {}

    try:
        with open(fname, 'r') as fh:
            extras['extras'] = [l.strip() for l in fh][1:]
    except:
        pass

    return extras


install_requires = get_requirements('requirements.txt')
setup_requires = get_requirements('requirements-setup.txt')
tests_require = get_requirements('requirements-tests.txt')
extras_require = get_extras('requirements-extras.txt')

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
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require=extras_require,
    #setup_requires=setup_requires,
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            'encode-podcast = podpublish.encode_podcast:main',
            'publish-podcast = podpublish.publish_podcast:main',
            'season-to-youtube = podpublish.season_to_youtube:main',
            'youtube-upload = youtube_upload.main:run',
        ],
        'gui_scripts' : [],
    },
    #test_suite='nose.collector',
)

################################################################################
# vim:et:ft=python:nowrap:sts=4:sw=4:ts=4
