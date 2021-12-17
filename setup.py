import glob

from setuptools import setup

# Available at setup time due to pyproject.toml
try:
    from pybind11.setup_helpers import Pybind11Extension as Extension
except ImportError:
    from setuptools import Extension

__version__ = "1.3.1"

setup(
    version=__version__,
    install_requires=["pybind11"],
    zip_safe=True,
    ext_modules=[
        Extension(
            "_pysilk", ["src/silk/_pysilk.cpp", "src/silk/codec.cpp", *glob.glob("src/silk/src/*.c")],
            library_dirs=["src/silk/"],
            include_dirs=["src/silk/interface"],
            define_macros=[('VERSION_INFO', __version__)]
        )
    ]
)
