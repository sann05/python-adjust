#!/usr/bin/env python
from pkg_resources import parse_requirements
from setuptools import setup
from pathlib import Path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


with Path("requirements.txt").open() as requirements_txt:
    install_requires = [
        str(requirement) for requirement in parse_requirements(requirements_txt)
    ]

setup(
    name="python-adjust",
    version="1.0.2",
    packages=["adjustapi"],
    description="Adjust.com REST API python implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sann05/python-adjust",
    author="Aliaksandr Sheliutsin",
    license="MIT",
    author_email="",
    install_requires=install_requires,
    keywords="adjust mobile measurement kpi api",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.5",
)
