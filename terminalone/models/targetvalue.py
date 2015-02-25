# -*- coding: utf-8 -*-
"""Provides region object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from ..errors import ClientError
from ..entity import Entity

class TargetValue(Entity):
	"""docstring for TargetValue."""
	collection = 'target_values'
	type = 'target_value'
	_relations = {
		'target_dimension',
	}

	# TODO attributes

	_pull = {
		'_type': None,
		'code': None,
		'id': int,
		'is_targetable': Entity._int_to_bool,
		'name': None,
		'target_dimension_id': int,
		'value': int,
	}
	def __init__(self, session, properties=None, **kwargs):
		super(TargetValue, self).__init__(session, properties, **kwargs)

	def save(self):
		raise ClientError('TargetValues are not editable.')
