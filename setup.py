#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="similarity",
    version="0.1.2",
    description="A collection of NLP tools for text-preprocessing tasks.",
    packages=find_packages(),
    install_requires=[
        d for d in open("requirements.txt").readlines() if not d.startswith("--")
    ],
    package_dir={"": "."},
    entry_points={
        "console_scripts": [
            "similarity = similarity_score.webservice:main",
        ]
    },
)
