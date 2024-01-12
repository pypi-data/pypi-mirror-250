#!/usr/bin/env python

from setuptools import find_packages, setup

from src import version

name = "doclifter"


setup(
    name=name,
    version=version,
    author="Eric S. Raymond",
    author_email="esr@thyrsus.com",
    maintainer="Mingzhe Zou",
    maintainer_email="zoumingzhe@outlook.com",
    long_description_content_type="text/plain",
    long_description=open("README").read(),
    url="https://gitlab.com/esr/doclifter",
    packages=find_packages(include=["src"]),
    scripts=[name],
)
