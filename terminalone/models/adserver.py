# -*- coding: utf-8 -*-
"""Provides ad server object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from ..entity import Entity

class AdServer(Entity):
	"""docstring for AdServer."""
	collection = 'ad_servers'
	type = 'ad_server'
	_relations = set()
	_pull = {
		'id': int,
		'name': None,
		'version': int,
	}
	_push = _pull.copy()
	def __init__(self, session, properties=None, **kwargs):
		super(AdServer, self).__init__(session, properties, **kwargs)
