from setuptools import setup, find_packages

from my_pip_package import __version__

setup(
    name='KevinPython',
    version=__version__,

    url='https://github.com/KevinTheCount/PipPackage',
    author='Kevin Counts',
    author_email='kevingcounts@gmail.com',

    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
