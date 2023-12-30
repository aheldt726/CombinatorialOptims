from setuptools import Extension, setup
from Cython.Build import cythonize

ext_modules = [
    Extension("bal_cython_assignment",
              sources=["bal_cython_assignment.pyx"],  # Unix-like specific
              )
]

setup(name="Bal_cython_assignment",
      ext_modules=cythonize(ext_modules, annotate=True))