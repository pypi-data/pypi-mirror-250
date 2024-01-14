# setup.py
from setuptools import setup, find_packages

setup(
    name="modularbuildingpy",
    version="0.2.2",
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
    install_requires=[
        "numpy==1.25.2",
        "pandas==2.1.0",
        "matplotlib==3.7.3",
        "openseespy==3.5.1.12",
        "ipyparallel==8.6.1",
        "pymetis==2023.1.1",
        "scipy==1.11.2",
        "shapely==2.0.2",
    ],
)
