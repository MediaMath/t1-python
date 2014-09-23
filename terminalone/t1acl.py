# -*- coding: utf-8 -*-
"""Provides target dimension object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import print_function
from .t1object import T1SubObject

class T1ACL(T1SubObject):
	"""docstring for T1TargetDimension."""
	collection = 'target_dimensions'
	type = 'target_dimension'
	_relations = {
		'strategy', 'target_value',
	}

	_pull = {
		'type': None,
		'editable': int,
		'strategy_id': int,
	}
	_readonly = T1SubObject._readonly.copy()
	def __init__(self, session, properties=None, **kwargs):
		super(T1ACL, self).__init__(session, properties, **kwargs)
	
	def save(self):
		raise T1ClientError('This object is not editable.')
