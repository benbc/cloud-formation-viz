#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='cloud_formation_viz',
    version='0.0.1',
    description='Visualise cloudformation templates',
    long_description=open("README.md").read(),
    license='MIT',
    author='Ben Butler-Cole',
    author_email='ben@bridesmere.com',
    url='https://github.com/benbc/cloud-formation-viz',
    packages=find_packages(exclude=['tests']),
    entry_points={
        "console_scripts": [
            "cfviz=cloud_formation_viz.main:main"
        ]
    },
    python_requires='>=3.7',
    install_requires=[
        "pyyaml"
    ],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",

        "Development Status :: 4 - Beta"
    ],
    include_package_data=True,
    zip_safe=False,
    keywords=[
        'yaml', 'json', 'cloudformation', 'graphviz', 'dot'
    ]
)
