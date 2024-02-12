# coding: utf-8
# 2023 En-Kun Li

from distutils.core import setup, Extension
import numpy as np
import sys

argv_replace = []

gsl_prefix = '/usr'

for arg in sys.argv:
    if arg.startswith('--with-gsl='):
        gsl_prefix = arg.split('=', 1)[1]
    else:
        argv_replace.append(arg)
sys.argv = argv_replace

lib_gsl_dir = gsl_prefix+"/lib"
include_gsl_dir = gsl_prefix+"/include"

# define the extension
extension_module = Extension(
        'pyEccentricFD.libEccFD', # name of the lib
        sources=['src/InspiralEccentricFD.c', 
        'src/InspiralEccentricFDBasic.c', 
        'src/InspiralOptimizedCoefficientsEccentricityFD.c'],
        include_dirs=['include', include_gsl_dir, np.get_include()],  # Add any necessary include directories
        libraries=['gsl', 'gslcblas', 'm'],  # Add any necessary libraries
        library_dirs=['lib', lib_gsl_dir],  # Add any necessary library directories
        extra_compile_args=["-std=c99"],
        )

setup(
    name='pyEccentricFD',
    version='0.0.1',
    author = 'Han Wang',
    description='Description of your package',
    ext_modules=[extension_module],
    packages = ['pyEccentricFD']
)
