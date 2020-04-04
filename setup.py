#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


extras_require = {
    "test": ["pytest>=4.6.3,<5.0.0", "pytest-cov>=2.7.1,<3.0.0"],
    "lint": [
        "mypy>=0.761,<1.0",
        "black>=19.3b0",
        "isort>=4.3.21",
        "flake8>=3.7.7,<4.0.0",
    ],
    "dev": ["tox>=3.13.2,<4.0.0", "wheel"],
}

extras_require["dev"] = (
    extras_require["test"] + extras_require["lint"] + extras_require["dev"]
)


setuptools.setup(
    name="crypto-toy",
    version="0.0.1",
    author="Kevin Mai-Hsuan Chia",
    author_email="kevin.mh.chia@gmail.com",
    description="A toy implementation of cryptography primitives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mhchia/py-crypto-toy",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=[],
    extras_require=extras_require,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
