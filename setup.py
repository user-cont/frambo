import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def get_requirements():
    """Parse all packages mentioned in the 'requirements.txt' file."""
    with open('requirements.txt') as file_stream:
        return file_stream.read().splitlines()


setup(
    name='frambo',
    version='0.0.3',
    packages=find_packages(exclude=['tests']),
    install_requires=get_requirements(),
    url='https://github.com/user-cont/frambo',
    license='GPLv3+',
    author='Usercont',
    author_email='user-cont-team@redhat.com',
    package_data={'frambo': [os.path.join('data', 'schemas', '*.json'),
                             os.path.join('data', 'defaults', '*.json')]},
)
