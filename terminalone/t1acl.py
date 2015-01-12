# -*- coding: utf-8 -*-
"""Provides acl object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from .t1error import ClientError
from .t1object import T1SubObject

class T1ACL(T1SubObject):
	"""docstring for T1ACL."""
	collection = 'acl'
	type = 'acl'
	_pull = {
		'_type': None,
		'editable': None,
	}

	def __init__(self, session, properties=None, **kwargs):
		for key,value in properties.iteritems():
			if '_id' in key:
				self._pull[key] = int
		super(T1ACL, self).__init__(session, properties, **kwargs)
	
	def save(self):
		raise ClientError('This object is not editable.')
