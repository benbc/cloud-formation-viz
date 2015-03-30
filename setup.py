#!/usr/bin/env python

from setuptools import setup


setup(name='cfviz',
      version='0.0.0',
      description='Python Distribution Utilities',
      author='Ben Butler-Cole',
      author_email='ben@bridesmere.com',
      url='https://github.com/benbc/cloud-formation-viz',
      py_modules=['cfviz'],
      entry_points={"console_scripts": ["cfviz = cfviz:main"]},
      classifiers=["Environment :: Console",
                   "Intended Audience :: Developers",
                   "Operating System :: Unix",
                   "Operating System :: POSIX",
                   "Programming Language :: Python",
                   "Development Status :: 4 - Beta"]
     )
