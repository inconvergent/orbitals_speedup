#!/usr/bin/python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy

_extra = ['-O3']

extensions = [
  Extension('speedup',
            sources = ['./src/speedup.pyx'],
            extra_compile_args = _extra
  )
]

setup(
  name = "speedup",
  cmdclass={'build_ext' : build_ext},
  include_dirs = [numpy.get_include()],
  ext_modules = cythonize(extensions,include_path = [numpy.get_include()])
)
