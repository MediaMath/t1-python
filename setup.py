#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
import os
import sys
import subprocess
from distutils.util import convert_path


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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

metadata = {}
ver_path = convert_path('terminalone/metadata.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), metadata)


def check_pip():
    st = subprocess.check_output('pip search {}'.format(metadata['__name__']), shell=True)
    pip_version = st[st.index('(')+1: st.index(')')]
    print(pip_version)
    if pip_version == metadata['__version__']:
        print('version {} already published. '
              'Modify metadata.py to update version and commit.'
              .format(pip_version))
        sys.exit()

if sys.argv[-1] == 'publish':
    check_pip()
    os.system("python setup.py sdist")
    filename = "TerminalOne-{}.tar.gz".format(metadata['__version__'])
    print('Uploading {}'.format(filename))
    os.system("twine upload dist/{}".format(filename))
    print("Did you remember to tag the release? ./setup.py tag")
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (metadata['__version__'], metadata['__version__']))
    os.system("git push --tags")
    sys.exit()

setup(
    name=metadata['__name__'],
    version=metadata['__version__'],
    author=metadata['__author__'],
    author_email='prasanna@mediamath.com',
    url='http://www.mediamath.com',
    description="A package for interacting with MediaMath's TerminalOne API.",
    long_description=fread('README.rst'),
    packages=packages,
    install_requires=requirements,
    platforms=['any'],
    license=fread('LICENSE'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
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
