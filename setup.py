#!/usr/bin/env python

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

packages = ['t1apicore']

requirements = ['requests']

setup(name='t1apicore',
		version=t1apicore.__version__,
		author='Prasanna Swaminathan',
		author_email='pswaminathan@mediamath.com',
		url='http://www.mediamath.com',
		description="A package for interacting with MediaMath's TerminalOne API."
		long_desription=open('README.md').read()
		packages=packages,
		install_requires=requrements,
		platforms=['any'],
)
