# -*- coding: utf-8 -*-
"""Provides ad server object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import T1Object

class T1AdServer(T1Object):
	"""docstring for T1AdServer."""
	collection = 'ad_servers'
	type = 'ad_server'
	_relations = set()
	_pull = {
		'id': int,
		'name': str,
		'version': int,
	}
	_push = _pull.copy()
	_readonly = T1Object._readonly.copy()
	def __init__(self, auth, properties=None, **kwargs):
		super(T1AdServer, self).__init__(auth, properties, **kwargs)
