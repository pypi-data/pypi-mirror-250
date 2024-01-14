# setup.py
from setuptools import setup, find_packages

setup(
    name="ModularBuildingPy",
    version="0.2",
    packages=find_packages(where="src"),
    description="A python module to create linear or nonlinear numerical models for volumetric modular steel buildings using the finite element method (OpenSeesPy).",
    long_description=open("README.rst").read(),
    author="Mehmet Baris Batukan",
    author_email="mbbatu@hotmail.com",
    url="https://github.com/mbbatukan/ModularBuildingPy.git",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
