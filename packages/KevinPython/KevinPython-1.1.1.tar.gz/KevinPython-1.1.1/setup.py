from setuptools import setup

from my_pip_package import __version__

setup(
    name='KevinPython',
    version=__version__,

    url='https://github.com/KevinTheCount/PipPackage',
    author='Kevin Counts',
    author_email='kevingcounts@gmail.com',

    py_modules=['my_pip_package'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
