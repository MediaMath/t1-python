# -*- coding: utf-8 -*-
"""Provides concept object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import T1Object

class T1Concept(T1Object):
	"""docstring for T1Concept."""
	collection = 'concepts'
	type = 'concept'
	_relations = {
		'advertiser',
	}
	_pull = {
		'advertiser_id': int,
		'created_on': T1Object._strpt,
		'id': int,
		'name': str,
		'status': T1Object._int_to_bool,
		'updated_on': T1Object._strpt,
		'version': int,
	}
	_push = _pull.copy()
	_push.update({
		'status': int,
	})
	_readonly = T1Object._readonly.copy()
	def __init__(self, auth, properties=None, **kwargs):
		super(T1Concept, self).__init__(auth, properties, **kwargs)
