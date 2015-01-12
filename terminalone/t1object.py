# -*- coding: utf-8 -*-
"""Provides base object for T1 data classes.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import, division
from datetime import datetime
import warnings
from .t1connection import T1Connection
from .t1error import ClientError
from .vendor.six import six


class T1Object(T1Connection):
	"""Superclass for all the various T1 entities.

	Implements methods for data validation and saving to T1.
	"""
	_readonly = {'id', 'build_date', 'created_on',
					'_type', # _type is used because "type" is taken by T1User.
					'updated_on', 'last_modified'}
	def __init__(self, session, properties=None, *args, **kwargs):
		"""Passes session information to underlying connection and validates properties passed in.
		
		T1Object, or any entity deriving from it, should never be instantiated directly.
		`T1` class should, with session information, instantiate the relelvant
		subclass.
		"""

		# __setattr__ is overridden below. So, to set self.properties as an empty
		# dict, we need to use the built-in __setattr__ method; thus, super()
		super(T1Object, self).__init__(create_session=False, **kwargs)
		super(T1Object, self).__setattr__('session', session)
		if properties is None:
			super(T1Object, self).__setattr__('properties', {})
			return
		# This block will only execute if properties is given
		for attr, val in six.iteritems(properties):
			if self._pull.get(attr) is not None:
				properties[attr] = self._pull[attr](val)
		super(T1Object, self).__setattr__('properties', properties)

	def __getitem__(self, attribute):
		"""DEPRECATED way of retrieving properties like with dictionary"""
		warnings.warn(('Accessing entity like a dictionary will be deprecated; '
							'please discontinue use.'),
						DeprecationWarning, stacklevel=2)
		if attribute in self.properties:
			return self.properties[attribute]
		else:
			raise AttributeError(attribute)

	def __setitem__(self, attribute, value):
		"""DEPRECATED way of setting properties like with dictionary"""
		warnings.warn(('Accessing entity like a dictionary will be deprecated; '
							'please discontinue use.'),
						DeprecationWarning, stacklevel=2)
		self.properties[attribute] = self._pull[attribute](value)

	def __getattr__(self, attribute):
		if attribute in self.properties:
			return self.properties[attribute]
		else:
			raise AttributeError(attribute)
	def __setattr__(self, attribute, value):
		if self._pull.get(attribute) is not None:
			self.properties[attribute] = self._pull[attribute](value)
		else:
			self.properties[attribute] = value

	def __getstate__(self):
		"""Custom pickling. TODO"""
		return super(T1Object, self).__getstate__()
	def __setstate__(self, state):
		"""Custom depickling. TODO"""
		return super(T1Object, self).__setstate__(state)

	@staticmethod
	def _int_to_bool(value):
		return bool(int(value))

	@staticmethod
	def _enum(all_vars, default):
		def get_value(test_value):
			if test_value in all_vars:
				return test_value
			else:
				return default
		return get_value

	@staticmethod
	def _strpt(ti):
		if isinstance(ti, datetime):
			return ti
		return datetime.strptime(ti, "%Y-%m-%dT%H:%M:%S")

	@staticmethod
	def _strft(ti):
		return datetime.strftime(ti, "%Y-%m-%dT%H:%M:%S")

	@staticmethod
	def _valid_id(id_):
		try:
			myid = int(id_)
		except (ValueError, TypeError):
			return False
		if myid < 1:
			return False
		return True

	def _validate_read(self, data):
		for key, value in six.iteritems(data):
			if key in self._pull:
				data[key] = self._pull[key](value)
		return data

	def _validate_write(self, data):
		if 'version' not in data and 'id' in self.properties:
			data['version'] = self.version
		for key, value in six.iteritems(data.copy()):
			if key in self._readonly or key in self._relations:
				del data[key]
			else:
				if self._push.get(key) is not None:
					data[key] = self._push[key](value)
				else:
					data[key] = value
		return data

	def _update_self(self, entity):
		for key, value in six.iteritems(entity):
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
			raise ClientError('Entity ID not given')
		url  = '/'.join([self.api_base, self.collection, str(self.id), 'history'])
		history = self._get(url)
		return history[0]

class T1SubObject(T1Object):
	def save(self, data=None):
		if self.properties.get('id'):
			url = '/'.join([self.api_base, self.parent, self.parent_id,
							self.collection, self.id])
		else:
			url = '/'.join([self.api_base, self.parent,
							self.parent_id, self.collection])
		if data is not None:
			data = self._validate_write(data)
		else:
			data = self._validate_write(self.properties)
		entity = self._post(url, data=data)[0][0]
		self._update_self(entity)

