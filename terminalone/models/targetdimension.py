# -*- coding: utf-8 -*-
"""Provides target dimension object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from ..errors import ClientError
from ..entity import SubEntity
from .targetvalue import TargetValue
from ..utils import PATHS

class TargetDimension(SubEntity):
	"""docstring for TargetDimension."""
	collection = 'target_dimensions'
	resource = 'target_dimension'
	_relations = {
		'strategy', 'target_value',
	}

	_pull = {
		'_type': None,
		'exclude': None,
		'include': None,
	}
	_push = _pull
	def __init__(self, session, properties=None, **kwargs):
		super(TargetDimension, self).__init__(session, properties, **kwargs)
		self.environment = kwargs['environment']
		for index, ent_dict in enumerate(self.exclude):
			self.exclude[index] = TargetValue(self.session,
				properties=ent_dict, environment=self.environment)
		for index, ent_dict in enumerate(self.include):
			self.include[index] = TargetValue(self.session,
				properties=ent_dict, environment=self.environment)

	def save(self, data=None, **kwargs):
		"""Saves the TargetDimension object.

		data: optional dict of properties
		"""
		if 'obj' in kwargs:
			import warnings
			warnings.warn('The obj flag is deprecated; discontinue use.',
						  DeprecationWarning, stacklevel=2)
		if data is None:
			data = {}

		data.update({
			'exclude': [location.id if isinstance(location, TargetValue) 
									else location for location in self.exclude],
			'include': [location.id if isinstance(location, TargetValue)
									else location for location in self.include]
		})

		return super(TargetDimension, self).save(data=data)

	def add_to(self, group, target):
		l = ['target_values', 0]
		if isinstance(target, int):
			target = [target,]
		elif hasattr(target, '__iter__'):
			for child_id in target:
				l[1] = str(child_id)
				entities, __ = super(TargetDimension, self)._get(PATHS['mgmt'], '/'.join(l))
				group.append(TargetValue(self.session,
										 properties=next(entities),
										 environment=self.environment))
		else:
			raise ClientError('add_to target should be an int or iterator')



	def remove_from(self, group, target):
		target_values = dict((target_value.id, target_value) 
								for target_value in group)
		if isinstance(target, list):
			for child_id in target:
				try:
					group.remove(target_values[child_id])
				except ValueError:
					raise ClientError('Target value with ID {0} not in given group.'.format(child_id))
		if isinstance(target, int):
			try:
				group.remove(target_values[target])
			except ValueError:
				raise ClientError('Target value with ID {0} not in given group.'.format(target))
