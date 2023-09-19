#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="similarity",
    version="0.1.2",
    description="Compute the similarity between two words or sentences.",
    packages=find_packages(),
    install_requires=[
        d for d in open("requirements.txt").readlines() if not d.startswith("--")
    ],
    package_dir={"": "."},
    entry_points={
        "console_scripts": [
            "similarity = main:main",
        ]
    },
)
