# -*- coding: utf-8 -*-
"""Provides target dimension object.

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
			self.subob_class = subob_class
			self.environment = kwargs['environment']
			for index, ent_dict in enumerate(self.exclude):
				self.exclude[index] = subob_class(self.session,
					properties=ent_dict, environment=self.environment)
			for index, ent_dict in enumerate(self.include):
				self.include[index] = subob_class(self.session,
					properties=ent_dict, environment=self.environment)

	def save(self, data=None):
		if self.properties.get('id'):
			url = '/'.join([self.api_base, self.parent, str(self.parent_id),
							self.collection, str(self.id)])
		else:
			url = '/'.join([self.api_base, self.parent,
							str(self.parent_id), self.collection])
		if data is not None:
			data = self._validate_write(data)
		else:
			data = {
				'exclude': [target_value.id for target_value in self.exclude],
				'include': [target_value.id for target_value in self.include]
			}
		entity = self._post(url, data=data)[0][0]

	def add_to(self, group, target):
		url = self.api_base + '/target_values/'
		if isinstance(target, list):
			for subob_id in target:
				entities, ent_count = self._get(url+str(subob_id))
				group.append(self.subob_class(self.session, properties=entities[0], environment=self.environment))
		elif isinstance(target, int):
			entities, ent_count = self._get(url+str(target))
			group.append(self.subob_class(self.session, properties=entities[0], environment=self.environment))

	def remove_from(self, group, target):
		target_values = dict((target_value.id, target_value) 
								for target_value in group)
		if isinstance(target, list):
			for subob_id in target:
				try:
					group.remove(target_values[subob_id])
				except ValueError:
					print 'Target value with ID {0} not in given group.'.format(subob_id)
		if isinstance(target, int):
			try:
				group.remove(target_values[target])
			except ValueError:
				print 'Target value with ID {0} not in given group.'.format(target)

	def _validate_write(self, data):
		if 'version' not in data and 'id' in self.properties:
			data['version'] = self.version
		for key, value in data.copy().iteritems():
			if key in self._readonly or key in self._relations:
				del data[key]
			else:
				if key in self._push:
					data[key] = self._push[key](value)
		return data
