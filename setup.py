import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    install_requires=["django>=4.0.0",
                      "djangorestframework",
                      "djangorestframework-camel-case==1.3.0",
                      "drf-spectacular",
                      "prodict"],
    package_dir={'': 'src'},
    packages=['fast_api'],
)
