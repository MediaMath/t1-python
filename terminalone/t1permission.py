# -*- coding: utf-8 -*-
"""Provides permission object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1error import T1ClientError
from .t1object import T1SubObject

class T1Permission(T1SubObject):
	"""docstring for T1Permission."""
	collection = 'permissions'
	type = 'permission'
	
	_pull = {
		'_type': None,
		'advertiser': None,
		'agency': None,
		'organization': None,
		'edit_data_definition': int,
		'view_data_definition': int,
		'edit_segments': int,
		'edit_campaigns': int,
		'access_internal_fees': int,
		'edit_margins_and_performance': int,
		'view_organizations': int,
		'view_segments': int,
		'view_dmp_reports': int,
		'type': None,
		'role': None,
		'scope': None,
	}

	def __init__(self, session, properties=None, **kwargs):
		super(T1Permission, self).__init__(session, properties, **kwargs)

	def save(self):
		raise T1ClientError('Temporarily not editable - update coming soon!')
