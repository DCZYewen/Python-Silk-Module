import glob

from setuptools import setup
from setuptools.command.test import test as tester

# Available at setup time due to pyproject.toml
try:
    from pybind11.setup_helpers import Pybind11Extension as Extension
except ImportError:
    from setuptools import Extension

__version__ = "1.4.0"


class PyTest(tester):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        tester.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        tester.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        exit(errno)


setup(
    version=__version__,
    install_requires=["pybind11"],
    tests_require=['pytest'],
    cmdclass={"test": PyTest},
    zip_safe=True,
    ext_modules=[
        Extension(
            "_pysilk", ["src/silk/_pysilk.cpp", "src/silk/codec.cpp", *glob.glob("src/silk/src/*.c")],
            include_dirs=["src/silk/interface"],
            define_macros=[('VERSION_INFO', __version__)]
        )
    ]
)
