import glob
from distutils import log
from distutils.dep_util import newer_group
from distutils.errors import DistutilsSetupError
from sys import version_info

from setuptools import setup
from setuptools.command.test import test as tester

# Available at setup time due to pyproject.toml

try:
    from pybind11.setup_helpers import Pybind11Extension as Extension
    from pybind11.setup_helpers import build_ext
except ImportError:
    from setuptools import Extension
    from distutils.command.build_ext import build_ext

__version__ = "1.5.0"
basic_dependency = ["pybind11", "setuptools"]

if version_info.major != 3 or version_info.minor < 6:
    raise RuntimeError("pysilk only support python 3.6 or newer")


class CustomBuilder(build_ext):
    def build_extension(self, ext):
        sources = ext.sources
        if sources is None or not isinstance(sources, (list, tuple)):
            raise DistutilsSetupError(
                "in 'ext_modules' option (extension '%s'), "
                "'sources' must be present and must be "
                "a list of source filenames" % ext.name)
        sources = list(sources)
        ext_path = self.get_ext_fullpath(ext.name)
        depends = sources + ext.depends
        if not (self.force or newer_group(depends, ext_path, 'newer')):
            log.debug("skipping '%s' extension (up-to-date)", ext.name)
            return
        else:
            log.info("building '%s' extension", ext.name)

            # First, scan the sources for SWIG definition files (.i), run
        # SWIG on 'em to create .c files, and modify the sources list
        # accordingly.
        sources = self.swig_sources(sources, ext)

        # Next, compile the source code to object files. 

        # XXX not honouring 'define_macros' or 'undef_macros' -- the
        # CCompiler API needs to change to accommodate this, and I
        # want to do one thing at a time! 

        # Two possible sources for extra compiler arguments:
        #   - 'extra_compile_args' in Extension object
        #   - CFLAGS environment variable (not particularly
        #     elegant, but people seem to expect it and I
        #     guess it's useful)
        # The environment variable should take precedence, and
        # any sensible compiler will give precedence to later
        # command line args.  Hence we combine them in order:
        extra_args = ext.extra_compile_args or []

        macros = ext.define_macros[:]
        for undef in ext.undef_macros:
            macros.append((undef,))

            # split sources
        cxx_files = []
        for s in sources:  # type: str
            if s.endswith(".cpp"):
                sources.remove(s)
                cxx_files.append(s)

        c_build_args = []
        for e in extra_args:
            if not e.startswith("-std="):
                c_build_args.append(e)

        objects = self.compiler.compile(sources,
                                        output_dir=self.build_temp,
                                        macros=macros,
                                        include_dirs=ext.include_dirs,
                                        debug=self.debug,
                                        extra_postargs=c_build_args,
                                        depends=ext.depends)

        objects += self.compiler.compile(cxx_files,
                                         output_dir=self.build_temp,
                                         macros=macros,
                                         include_dirs=ext.include_dirs,
                                         debug=self.debug,
                                         extra_postargs=extra_args,
                                         depends=ext.depends)

        # XXX outdated variable, kept here in case third-part code
        # needs it.
        self._built_objects = objects[:]

        # Now link the object files together into a "shared object" --
        # of course, first we have to figure out all the other things
        # that go into the mix.
        if ext.extra_objects:
            objects.extend(ext.extra_objects)
        extra_args = ext.extra_link_args or []

        # Detect target language, if not provided
        language = ext.language or self.compiler.detect_language(sources)

        self.compiler.link_shared_object(
            objects, ext_path,
            libraries=self.get_libraries(ext),
            library_dirs=ext.library_dirs,
            runtime_library_dirs=ext.runtime_library_dirs,
            extra_postargs=extra_args,
            export_symbols=self.get_export_symbols(ext),
            debug=self.debug,
            build_temp=self.build_temp,
            target_lang=language)


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
