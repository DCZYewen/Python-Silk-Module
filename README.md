Python silk module. --- pysilk ---
=============

APIs
------------

See `test\test.py`.
```
import pysilk as m
m.silkEncode(buf , 24000)
m.silkDecode(buf , 24000)
#the first param is buffer of data, the second param is sample rate.
```
In PyCharm and other IDEs like vscode, the param is supposed to be
highlighted. And a breif intro in appended.


Installation
------------

**On Unix (Linux, OS X)**

 - clone this repository
 - `pip install .`

**On Windows (Requires Visual Studio 2015)**

 - For Python 3.5+:
     - clone this repository
     - `pip install .`
 - For Python 2.7:

   No longer supported.

   Note that this requires the user building `pysilk` to have registry edition
   rights on the machine, to be able to run the `vcvarsall.bat` script.


Building the documentation
--------------------------

Documentation for the example project is generated using Sphinx. Sphinx has the
ability to automatically inspect the signatures and documentation strings in
the extension module to generate beautiful documentation in a variety formats.
The following command generates HTML-based reference documentation; for other
formats please refer to the Sphinx manual:

 - `cd ./docs`
 - `make html`

Notices
--------------------------

I only tested it on Windows 10, Visual Studio 2019, python3.8. If you are interested in
reporting issues on build errors or bugs, please open an issue or email me at contact@basicws.net.

License
-------

All the licenses are in the LICENSE file. This project is also
released under BSD lisence.


[`cibuildwheel`]:          https://cibuildwheel.readthedocs.io
