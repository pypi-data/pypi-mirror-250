# Copyright 2024 Daniel Park, MIT License

import re
from setuptools import find_packages
from setuptools import setup


def get_version():
    filename = "kotokenizer/__init__.py"
    with open(filename) as f:
        match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M)
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


def get_long_description():
    with open("README.md", encoding="UTF-8") as f:
        long_description = f.read()
        return long_description


version = get_version()

setup(
    name="kotokenizer",
    version="0.1.0",
    author="daniel park",
    author_email="parkminwoo1991@gmail.com",
    description="Korean tokenizer, sentence classification, and spacing model.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/dsdanielpark/ko-tokenizer",
    packages=find_packages(exclude=[]),
    python_requires=">=3.6",
    install_requires=[
    ],
    keywords="Python, Tokenizer, Korean, Korean Tokenizer, NLP, Natural Language Process, LLM, Large Language Model",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Natural Language :: Korean",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)