from setuptools import setup, find_packages

DESCRIPTION: str = "A Python package for processing data from .zenf files."
LONG_DESCRIPTION: str = "A Python package providing useful and important features to process data from .zenf files and to parse them to local python types."

setup(
    name="zendatastorage",
    author="SpiralCreationsPyPi",
    author_email="SpiralCreationsPyPi@proton.me",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version="1.0.9",
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