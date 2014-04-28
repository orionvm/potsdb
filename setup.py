import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "potsdb",
    version = "0.0.1",
    author = "Alex Sharp, Chris McClymont",
    author_email = "alex.sharp@orionvm.com",
    description = ("A Python client for OpenTSDB which creates a separate "
                   "thread for TCP communication."),
    license = "GNU GPL",
    keywords = "opentsdb, tsdb, time series",
    url = "http://github.com/orionvm/potsdb",
    py_modules=['potsdb'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
