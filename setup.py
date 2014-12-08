#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Adrian Perez <aperez@igalia.com>
#
# Distributed under terms of the GPLv3 license.

from setuptools import setup, find_packages
from setuptools import find_packages
from codecs import open
from os import path
import sys

# Prefer the local version of nihil.metadata
sys.path.insert(0, path.abspath(path.dirname(__file__)))
from nihil.metadata import metadata


def file_contents(*relpath):
    with open(path.join(path.dirname(__file__), *relpath), "rU",
            encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    setup(
        name=metadata.package,
        version=metadata.version,
        description=metadata.description,
        long_description=file_contents("README.rst"),
        author=metadata.main_author_name,
        author_email=metadata.main_author_email,
        url=metadata.url,
        packages=find_packages(),
        tests_require=metadata.test_requirements,
        install_requires=metadata.requirements,
        extras_require=metadata.extra_requirements,
        license=metadata.license,
        classifiers=metadata.classifiers,
        test_suite="nihil.test",
        include_package_data=True,
        entry_points={ "console_scripts": metadata.entry_points },
    )
