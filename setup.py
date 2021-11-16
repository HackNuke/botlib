# This file is placed in the Public Domain.


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="botlib",
    version="143",
    url="https://github.com/bthate/botlib",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="python3 bot library",
    long_description=read(),
    license="Public Domain",
    packages=["bot"],
    include_package_data=True,
    data_files=[("etc/rc.d", ["rc.d/botd",],)],
    scripts=["bin/bot", "bin/botc", "bin/botd"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
