from distutils.core import setup
from Cython.Build import cythonize


setup(name='mc_mics_v2_test',
      ext_modules=cythonize("mc_mics_v2_test.pyx"))
