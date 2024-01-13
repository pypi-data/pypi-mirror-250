from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

ext_modules = Extension('core.*', ['core/*.py']),

setup(
    name='proalgotrader',
    version='1.0',
    ext_modules=cythonize(ext_modules),
    include_dirs=["core"],
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
    ],
)
