# -*- coding: utf-8 -*-
"""Provides target dimension object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1error import T1ClientError
from .t1object import T1SubObject
from .t1targetvalue import T1TargetValue

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
	def __init__(self, session, properties=None, **kwargs):
		super(T1TargetDimension, self).__init__(session, properties, **kwargs)
		self.environment = kwargs['environment']
		for index, ent_dict in enumerate(self.exclude):
			self.exclude[index] = T1TargetValue(self.session,
				properties=ent_dict, environment=self.environment)
		for index, ent_dict in enumerate(self.include):
			self.include[index] = T1TargetValue(self.session,
				properties=ent_dict, environment=self.environment)
	
	def save(self, data=None, **kwargs):
		"""Saves the TargetDimension object.
		
		The data keyword expects dictionary of properties to POST to T1.
		
		Arguments are optional.
		"""
		if self.properties.get('id'):
			url = '/'.join([self.api_base, self.parent, str(self.parent_id),
							self.collection, str(self.id)])
		else:
			url = '/'.join([self.api_base, self.parent,
							str(self.parent_id), self.collection])
		if data is not None:
			data = self._validate_write(data)
		else:
			if 'obj' in kwargs:
				import warnings
				warnings.warn('The obj flag is deprecated - please discontinue use.',
								DeprecationWarning, stacklevel=2)
			data = {
				'exclude': [location.id if isinstance(location, T1TargetValue) 
								else location for location in self.exclude],
				'include': [location.id if isinstance(location, T1TargetValue)
								else location for location in self.include]
			}
		entity = self._post(url, data=data)[0][0]
		self._update_self(entity)

	def add_to(self, group, target):
		url = self.api_base + '/target_values/'
		if isinstance(target, list):
			for child_id in target:
				entities, ent_count = self._get(url+str(child_id))
				group.append(T1TargetValue(self.session, properties=entities[0], environment=self.environment))
		elif isinstance(target, int):
			entities, ent_count = self._get(url+str(target))
			group.append(T1TargetValue(self.session, properties=entities[0], environment=self.environment))

	def remove_from(self, group, target):
		target_values = dict((target_value.id, target_value) 
								for target_value in group)
		if isinstance(target, list):
			for child_id in target:
				try:
					group.remove(target_values[child_id])
				except ValueError:
					raise T1ClientError('Target value with ID {0} not in given group.'.format(child_id))
		if isinstance(target, int):
			try:
				group.remove(target_values[target])
			except ValueError:
				raise T1ClientError('Target value with ID {0} not in given group.'.format(target))
