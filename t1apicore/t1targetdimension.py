# -*- coding: utf-8 -*-
"""Provides region object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import T1SubObject


class T1TargetDimension(T1SubObject):
	"""docstring for T1TargetDimension."""
	collection = 'target_dimensions'
	type = 'target_dimension'
	_relations = {
		'strategy', 'target_value',
	}

	_pull = {
		'_type': None,
		'exclude': None,
		'include': None,
	}
	_push = _pull.copy()
	_readonly = T1SubObject._readonly.copy()
	def __init__(self, session, subob_class=None, properties=None, **kwargs):
		super(T1TargetDimension, self).__init__(session, properties, **kwargs)
		if subob_class:
			for index, ent_dict in enumerate(self.properties['exclude']):
				self.properties['exclude'][index] = subob_class(self.session,
					properties=ent_dict, environment=kwargs['environment'])
			for index, ent_dict in enumerate(self.properties['include']):
				self.properties['include'][index] = subob_class(self.session,
					properties=ent_dict, environment=kwargs['environment'])
