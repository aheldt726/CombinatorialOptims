from setuptools import setup, Extension
from Cython.Build import cythonize
import Cython.Compiler.Options
import numpy

Cython.Compiler.Options.annotate = True

extensions = [
    Extension("*", ["*.pyx"],
              include_dirs=[numpy.get_include()])
]

setup(
    ext_modules=cythonize(extensions, annotate=True)
)
