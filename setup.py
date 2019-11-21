"""Setuptools package definition."""

from setuptools import find_packages, setup

version = {}
with open("document_merge_service/document_merge_service_metadata.py") as fp:
    exec(fp.read(), version)

setup(
    name=version["__title__"],
    version=version["__version__"],
    description=version["__description__"],
    author=version["__author__"],
    url=version["__url__"],
    license="MIT",
    packages=find_packages(),
)
