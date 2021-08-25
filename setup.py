# This file is place in the Public Domain.

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='130',
    url='https://github.com/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="python3 bot library",
    long_description=read(),
    license='Public Domain',
    packages=["bot"],
    scripts=["bin/bot"],
    zip_safe=True,
    include_package_data=True,
    data_files=[("man/man1/bot.1.gz", ["files/bot.1.gz"])],
    script=["bin/bot"],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
