#!/usr/bin/env python

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

packages = ['terminalone', 'terminalone.models', 'terminalone.vendor', 'terminalone.vendor.six']

requirements = ['requests>=2.3.0']

setup(
	name='TerminalOne',
	version='0.4.0a4',
	author='Prasanna Swaminathan',
	author_email='prasanna@mediamath.com',
	url='http://www.mediamath.com',
	description="A package for interacting with MediaMath's TerminalOne API.",
	long_description=open('README.rst').read(),
	packages=packages,
	install_requires=requirements,
	platforms=['any'],
)
