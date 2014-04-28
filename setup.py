import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "otsdb_sender",
    version = "0.0.1",
    author = "Alex Sharp, Chris McClymont",
    author_email = "alex.sharp@orionvm.com",
    description = ("A client to OpenTSDB which creates a separate thread for TCP "
                                   "communication."),
    license = "GNU GPL",
    keywords = "opentsdb, tsdb, time series",
    url = "http://github.com/orionvm/otsdb_sender",
    py_modules=['otsdb_sender'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
