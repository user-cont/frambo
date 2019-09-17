try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(name="foobarbot", version="0.0.1", packages=find_packages())
