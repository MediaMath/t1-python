# -*- coding: utf-8 -*-
"""
Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from .constants import filters
from .t1service import T1, T1Service

__author__ = 'Prasanna Swaminathan'
__copyright__ = 'Copyright 2014, Prasanna Swaminathan'
__version__ = '0.4.0a1'
__maintainer__ = 'Prasanna Swaminathan'
__email__ = 'prasanna@mediamath.com'
__status__ = 'Development'
__all__ = ['T1', 'T1Service']
