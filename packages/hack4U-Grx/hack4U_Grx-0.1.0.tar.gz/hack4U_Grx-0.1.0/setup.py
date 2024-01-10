#!/usr/bin/env python3

from setuptools import setup, find_packages

# Lleer el contenido de README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4U_Grx",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="David Martínez",
    description="Biblioteca para consultar cursos de hack4u",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)