# This file is placed in the Public Domain.

from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="botlib",
    version="140",
    url="https://github.com/bthate/botlib",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="python3 bot library",
    long_description=read(),
    license="Public Domain",
    packages=["bot"],
    zip_safe=True,
    include_package_data=True,
    data_files=[
        (
            "share/botlib/",
            [
                "files/bot.1.md",
                "files/bots",
                "files/bots.service",
            ],
        )
    ],
    scripts=["bin/bot"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
