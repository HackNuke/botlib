# This file is place in the Public Domain.

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='124',
    url='https://github.com/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="python3 bot library",
    long_description=read(),
    license='Public Domain',
    packages=["botl", "botmod", "bot"],
    namespace_package=["bot", "botmod"],
    zip_safe=True,
    scripts=["bin/botl"],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
