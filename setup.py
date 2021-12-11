import glob

from setuptools import setup, find_packages
# Available at setup time due to pyproject.toml
try:
    from pybind11.setup_helpers import Pybind11Extension as Extension
except ImportError:
    from setuptools import Extension

__version__ = "1.2.1"

ext_modules = [
    Extension(
        "_pysilk", ["src/_pysilk.cpp", "src/codec.cpp", *glob.glob("src/silk/src/*.c")],
        include_dirs=["src/silk/interface"],
        define_macros=[('VERSION_INFO', __version__)]
    )
]

setup(
    name="pysilk-mod",
    version=__version__,
    author="DCZYewen",
    author_email="contact@basicws.net",
    url="https://github.com/DCZYewen/Python-Silk-Module",
    description="Python silk decode/encoder",
    long_description="Python silk decode/encoder bindings using pybind11",
    packages=find_packages(),
    requires=["pybind11"],
    ext_modules=ext_modules,
    zip_safe=False
)
