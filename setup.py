#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def fread(fname):
    with open(os.path.join(CURRENT_DIR, fname)) as f:
        return f.read()


packages = [
    'terminalone',
    'terminalone.models',
    'terminalone.utils',
    'terminalone.vendor',
]

requirements = [
    'requests>=2.3.0',
    'requests-oauthlib>=0.5.0',
]

setup(
    name='TerminalOne',
    version='1.4.3',
    author='Prasanna Swaminathan',
    author_email='prasanna@mediamath.com',
    url='http://www.mediamath.com',
    description="A package for interacting with MediaMath's TerminalOne API.",
    long_description=fread('README.rst'),
    packages=packages,
    install_requires=requirements,
    platforms=['any'],
    license=fread('LICENSE'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    test_suite="tests",
)
