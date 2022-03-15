import glob
from sys import version_info

from setuptools import setup
from setuptools.command.test import test as tester

# Available at setup time due to pyproject.toml
try:
    from pybind11.setup_helpers import Pybind11Extension as Extension
    from custom_build import CustomBuilder
except ImportError:
    from setuptools import Extension

__version__ = "1.4.1"
basic_dependency = ["pybind11", "setuptools"]

if version_info.major != 3 or version_info.minor < 6:
    raise RuntimeError("pysilk only support python 3.6 or newer")


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

        exit(
            pytest.main(self.pytest_args)
        )


def get_compile_file_list():
    files = glob.glob("src/silk/src/*.c")
    files.extend(["src/silk/_pysilk.cpp", "src/silk/codec.cpp"])
    return files


setup(
    version=__version__,
    requires=basic_dependency,
    tests_require=basic_dependency + ["pytest"],
    cmdclass={"test": PyTest, "build_ext": CustomBuilder},
    zip_safe=True,
    ext_modules=[
        Extension(
            "pysilk.coder", get_compile_file_list(),
            include_dirs=["src/silk/interface"],
            define_macros=[('VERSION_INFO', __version__)],
            extra_compile_args=["-std=c++11"]
        )
    ]
)
