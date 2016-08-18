import os
from setuptools import setup, find_packages
import csg # to get the package version number

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pycsg',
    version=csg.__version__,
    description='Constructive Solid Geometry (CSG)',
    long_description=read('README.md'),
    keywords = "constructive solid geometry csg utilities",

    author='Tim Knip',
    author_email='tim@floorplanner.com',
    url='https://github.com/timknip/pycsg',

    install_requires = [],
    packages=find_packages(),
    license = "MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
