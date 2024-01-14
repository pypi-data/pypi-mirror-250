|python| |MIT| |black|

.. |python| image:: https://img.shields.io/badge/python-3.11-blue.svg
   :target: https://github.com/mbbatukan/ModularBuildingPy/
   :alt: Python

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

ModularBuildingPy
=================

ModularBuildingPy is a Python module designed to create linear or nonlinear numerical models for volumetric modular steel buildings using the finite element method. It leverages the power of OpenSeesPy, a Python library for the Open System for Earthquake Engineering Simulation (OpenSees).

Features
--------

- **Linear and Nonlinear Models**: Create both linear and nonlinear numerical models based on your specific requirements.
- **Volumetric Modular Steel Buildings**: Specifically designed for creating models of volumetric modular steel buildings.
- **Finite Element Method**: Uses the finite element method for creating numerical models, providing accurate and reliable results.
- **OpenSeesPy Integration**: Fully integrated with OpenSeesPy, allowing for advanced earthquake engineering simulations.

Installation
------------

You can install ModularBuildingPy using pip:

.. code-block:: bash

   pip install modularbuildingpy

Usage
-----

After installing the module, you can import it in your Python scripts as follows:

.. code-block:: python

   import modularbuildingpy as mbp

Code Style
----------

This project uses the `Black <https://black.readthedocs.io/en/stable/>`_ code formatter. To ensure consistency in code style, please run Black on any changes before committing:

.. code-block:: bash

   black .


Contributing
------------

Contributions are welcome! Please read the contributing guidelines first.

License
-------

ModularBuildingPy is licensed under the MIT License. See LICENSE for more information.