"""Setuptools package definition."""

from setuptools import find_packages, setup

setup(
    name="document_merge_service",
    version="0.0.0",
    author="Adfinis SyGroup AG",
    author_email="https://adfinis-sygroup.ch/",
    description="Merge Document Template Service",
    url="https://github.com/adfinis-sygroup/document-merge-service",
    license="MIT",
    packages=find_packages(),
)
