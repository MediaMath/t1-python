# -*- coding: utf-8 -*-
"""Provides target dimension object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import print_function
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

	def save(self, data=None, obj_flag=False):
		if self.properties.get('id'):
			url = '/'.join([self.api_base, self.parent, str(self.parent_id),
							self.collection, str(self.id)])
		else:
			url = '/'.join([self.api_base, self.parent,
							str(self.parent_id), self.collection])
		if data is not None:
			data = self._validate_write(data)
		else:
			if obj_flag:
				data = {
					'exclude': [target_value.id for target_value in self.exclude],
					'include': [target_value.id for target_value in self.include]
				}
			else:
				data = {
					'exclude': self.exclude,
					'include': self.include
				}
		entity = self._post(url, data=data)[0][0]

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
					print('Target value with ID {0} not in given group.'.format(child_id))
		if isinstance(target, int):
			try:
				group.remove(target_values[target])
			except ValueError:
				print('Target value with ID {0} not in given group.'.format(target))
