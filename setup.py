#!/usr/bin/env python

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

packages = ['terminalone',
			'terminalone.models',
			'terminalone.vendor',
			'terminalone.vendor.six']

requirements = ['requests>=2.3.0']

setup(
	name='TerminalOne',
	version='0.4.6',
	author='Prasanna Swaminathan',
	author_email='prasanna@mediamath.com',
	url='http://www.mediamath.com',
	description="A package for interacting with MediaMath's TerminalOne API.",
	long_description=open('README.rst').read(),
	packages=packages,
	install_requires=requirements,
	platforms=['any'],
	classifiers=[
		'Development Status :: 4 - Beta'
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Operating System :: OS Independent',
	],
)
