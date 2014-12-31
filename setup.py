from setuptools import setup

setup(
    name='cloud-formation-viz',
    version='0.0.1',
    description='Produce graphviz from a given CloudFormation template',
    long_description=open('README.rst').read(),
    author='Ben Butler-Cole',
    author_email='ben@bridesmere.com',
    scripts=['cfviz'],
    license='???', # FIXME Just what license is this under?
)
