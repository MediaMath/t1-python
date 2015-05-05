#!/usr/bin/env python

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
import os
import warnings

def long_description():
	import os
	CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
	rst = os.path.join(CURRENT_DIR, 'README.rst')
	if os.path.exists(rst):
		with open('README.rst') as f:
			return f.read()
	try:
		import pypandoc
	except ImportError:
		warnings.warn('pypandoc module not found; could not convert Markdown to RST')
		with open(os.path.join(CURRENT_DIR, 'README.md')) as f:
			return f.read()
	else:
		return pypandoc.convert('README.md', 'rst', format='md')

packages = [
	'terminalone',
	'terminalone.models',
	'terminalone.vendor',
	'terminalone.vendor.six',
]

requirements = ['requests>=2.3.0']

setup(
	name='TerminalOne',
	version='0.5.3',
	author='Prasanna Swaminathan',
	author_email='prasanna@mediamath.com',
	url='http://www.mediamath.com',
	description="A package for interacting with MediaMath's TerminalOne API.",
	long_description=long_description(),
	packages=packages,
	install_requires=requirements,
	platforms=['any'],
	classifiers=[
		'Development Status :: 4 - Beta',
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
