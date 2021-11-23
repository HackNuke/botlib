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
    data_files=[
                ("share/botd", ["files/botd.service",],)
                ('share/doc/botd', ['docs/aprogramming.rst',
                                    'docs/asource.rst',
                                    'docs/conf.py',
                                    'docs/index.rst',
                                    'docs/_templates/base.rst',
                                    'docs/_templates/class.rst',
                                    'docs/_templates/layout.html',
                                    'docs/_templates/module.rst'])],


    ],
    scripts=["bin/bot", "bin/botc", "bin/botctl", "bin/botd"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
