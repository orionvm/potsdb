from setuptools import setup, find_packages
from potsdb import __version__

try:
    from pypandoc import convert

    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

if __name__ == '__main__':
    project_name = "potsdb"
    setup(
        name=project_name,
        version=__version__,
        author="Alex Sharp, Chris McClymont",
        author_email="alex.sharp@orionvm.com",
        description=("A Python client for OpenTSDB which creates a separate "
                     "thread for TCP communication."),
        license="GNU GPL",
        keywords="opentsdb, tsdb, time series",
        url="http://github.com/orionvm/potsdb",
        packages=find_packages(),
        long_description=read_md('README.md'),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
        ],
        test_suite=project_name + '.tests',
    )
