Python silk module. --- pysilk ---
=============

Installation
------------

**On Unix (Linux, OS X)**

 - clone this repository
 - `pip install ./python_example`

**On Windows (Requires Visual Studio 2015)**

 - For Python 3.5+:
     - clone this repository
     - `pip install ./python_example`
 - For Python 2.7:

   Pybind11 requires a C++11 compliant compiler (i.e. Visual Studio 2015 on
   Windows). Running a regular `pip install` command will detect the version
   of the compiler used to build Python and attempt to build the extension
   with it. We must force the use of Visual Studio 2015.

     - clone this repository
     - `"%VS140COMNTOOLS%\..\..\VC\vcvarsall.bat" x64`
     - `set DISTUTILS_USE_SDK=1`
     - `set MSSdk=1`
     - `pip install ./python_example`

   Note that this requires the user building `python_example` to have registry edition
   rights on the machine, to be able to run the `vcvarsall.bat` script.


Building the documentation
--------------------------

Documentation for the example project is generated using Sphinx. Sphinx has the
ability to automatically inspect the signatures and documentation strings in
the extension module to generate beautiful documentation in a variety formats.
The following command generates HTML-based reference documentation; for other
formats please refer to the Sphinx manual:

 - `cd python_example/docs`
 - `make html`

Notices
--------------------------

I only tested it on Windows 10, Visual Studio 2019, python3.8. If you are interested in
reporting issues on build errors or bugs, please open an issue or email me at contact@basicws.net.

License
-------

pybind11 is provided under a BSD-style license that can be found in the LICENSE
file. By using, distributing, or contributing to this project, you agree to the
terms and conditions of this license.


[`cibuildwheel`]:          https://cibuildwheel.readthedocs.io
