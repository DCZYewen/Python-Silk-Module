import glob

from setuptools import setup
# Available at setup time due to pyproject.toml
try:
    from pybind11.setup_helpers import Pybind11Extension as Extension
except ImportError:
    from setuptools import Extension

__version__ = "1.2.2"

setup(
    name="pysilk-mod",
    version=__version__,
    author="DCZYewen",
    author_email="contact@basicws.net",
    url="https://github.com/DCZYewen/Python-Silk-Module",
    description="Python silk decode/encoder",
    long_description="Python silk decode/encoder bindings using pybind11",
    packages=["src/pysilk"],
    requires=["pybind11"],
    zip_safe=False,
    ext_modules=[
        Extension(
            "_pysilk", ["src/silk/_pysilk.cpp", "src/silk/codec.cpp", *glob.glob("src/silk/src/*.c")],
            include_dirs=["src/silk/interface"],
            define_macros=[('VERSION_INFO', __version__)]
        )
    ]
)
