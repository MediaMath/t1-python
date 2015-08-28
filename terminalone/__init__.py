# -*- coding: utf-8 -*-
"""
Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from .utils import filters
from .service import T1, T1Service
from . import errors
from .metadata import (__author__, __copyright__, __license__, __version__,
                       __maintainer__, __email__, __status__)

__all__ = ['T1', 'T1Service', 'filters', 'errors']
