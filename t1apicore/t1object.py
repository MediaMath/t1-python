# -*- coding: utf-8 -*-
"""Provides base object for T1 data classes.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import division#, absolute_import
from datetime import datetime
from math import ceil
from .t1connection import T1Connection


class T1Object(T1Connection):
	"""Superclass for all the various T1 Objects. Implements methods for """
	_readonly = {'id', 'build_date', 'created_on', '_type', # _type is used because "type" is taken by T1User.
						'updated_on', 'last_modified'}
	def __init__(self, auth, properties=None):
		super(T1Object, self).__init__(auth)

		# __setattr__ is overridden below. So, to set self.properties as an empty
		# dict, we need to use the built-in __setattr__ method; thus, super()
		super(T1Object, self).__setattr__('properties', {})
		if isinstance(properties, dict):
			for attr, val in properties.iteritems():
				try:
					self.properties[attr] = self._pull[attr](val)
				except KeyError:
					self.properties[attr] = val
				# setattr(self, attr, val)

	def __getitem__(self, attribute):
		if attribute in self.properties:
			return self.properties[attribute]
		else:
			raise AttributeError(attribute)
	def __setitem__(self, attribute, value):
		self.properties[attribute] = self._pull[attribute](value)

	def __getattr__(self, attribute):
		if attribute in self.properties:
			return self.properties[attribute]
		else:
			raise AttributeError(attribute)
	def __setattr__(self, attribute, value):
		try:
			self.properties[attribute] = self._pull[attribute](value)
		except KeyError:
			super(T1Object, self).__setattr__(attribute, value)

	@classmethod
	def _int_to_bool(cls, value):
		return bool(int(value))
	@classmethod
	def _enum(cls, all_vars, default):
		def get_value(test_value):
			if test_value in all_vars:
				return test_value
			else:
				return default
		return get_value
	@classmethod
	def _strpt(cls, ti):
		return datetime.strptime(ti, "%Y-%m-%dT%H:%M:%S")
	@classmethod
	def _strft(cls, ti):
		return datetime.strftime(ti, "%Y-%m-%dT%H:%M:%S")
	@classmethod
	def _valid_id(cls, id_):
		try:
			myid = int(id_)
		except (ValueError, TypeError):
			return False
		if myid < 1:
			return False
		return True
	def _validate_read(self, data):
		for key, value in data.iteritems():
			if key in self._pull:
				data[key] = self._pull[key](value)
		return data

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

	def _update_self(self, entity):
		for key, value in entity.iteritems():
			setattr(self, key, value)

	def save(self, data=None):
		if self.properties.get('id'):
			url = '/'.join([self.api_base, self.collection, str(self.id)])
		else:
			url = '/'.join([self.api_base, self.collection])
		if data is not None:
			data = self._validate_write(data)
		else:
			data = self._validate_write(self.properties)
		entity = self._post(url, data=data)[0][0]
		self._update_self(entity)

	def update(self, *args, **kwargs):
		return self.save(*args, **kwargs)

	def history(self):
		if not self.properties.get('id'):
			raise T1ClientError('Valid entity ID not given')
		url  = '/'.join([self.api_base, collection, str(self.id), 'history'])
		history = self._get(url)
		return history

# class T1Objects(object):
# 	pass
