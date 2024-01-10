import os
from setuptools import setup, find_packages

DESCRIPTION: str = "A Python package for processing data from .zenf files."
LONG_DESCRIPTION: str = ""
LONG_DESCRIPTION = """
A Python package providing useful and important features to process data from .zenf files and to parse them to local python types.

## Simple Use

#### Read Var from .zenf file

##### Test.zenf File

    ["TestVar"] = Hello;

#### Main.py File

    from zendatastorage import Interpret

    with open("Test.zenf", "r") as f:
        VarDict = Interpret(f)

    print(VarDict["TestVar"])

#### Output
    Hello
"""

setup(
    name="zendatastorage",
    author="SpiralCreationsPyPi",
    author_email="SpiralCreationsPyPi@proton.me",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version="1.0.101",
    packages=find_packages(),
    install_requires=["colorama"],
    keywords=[
        "Data Storage",
        "Storage",
        "Data"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent"
    ]
)