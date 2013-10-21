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
pass

class T1Object(T1Connection):
	"""Superclass for all the various T1 Objects. Implements methods for """
	_readonly = {'id', 'build_date',' created_on', '_type', # _type is used because "type" is taken by T1User.
						'updated_on', 'last_modified'}
	def __init__(self, auth, properties=None):
		super(T1Object, self).__init__(auth)
		# self.adama.auth = auth # Called by T1Service so auth should be there
		super(T1Object, self).__setattr__('properties', {})
		if isinstance(properties, dict):
			for attr, val in properties.iteritems():
				try:
					self.properties[attr] = self._pull[attr](val)
				except KeyError:
					self.properties[attr] = val
				# setattr(self, attr, val)
		pass
		# Get attribute definitions?
		# Get attribute default values?

	def __getitem__(self, attribute):
		if attribute in self.properties:
			return self.properties[attribute]
		else:
			raise AttributeError
	def __setitem__(self, attribute, value):
		self.properties[attribute] = self._pull[attribute](value)

	def __getattr__(self, attribute):
		if attribute in self.properties:
			return self.properties[attribute]
		else:
			raise AttributeError
	def __setattr__(self, attribute, value):
		try:
			self.properties[attribute] = self._pull[attribute](value)
		except KeyError:
			super(T1Object, self).__setattr__(attribute, value)

	@classmethod
	def _int_to_bool(cls, value):
		return bool(int(value))
	@classmethod
	def _bool_to_int(cls, value): # Necessary? Don't think so...
		return int(bool(value)) # int(True) = 1 and vice-versa
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
		for key, value in data.copy().iteritems():
			if key in self._readonly:
				del data[key]
			if key in self._push:
				data[key] = self._push[key](value)
		return data
	
	# def get_one(self, entity_id, collection=None):
	# 	"""Wrapper for _get that enforces type.
		
	# 	banana
	# 	"""
	# 	if collection is None:
	# 		collection = self.collection
	# 	if collection not in T1Object.t1_collections:
	# 		raise T1ClientError('Invalid collection.')
	# 	if not self._valid_id(entity_id):
	# 		raise T1ClientError('Entity called is not a valid entity ID')
	# 	url = '/'.join([self.api_base, collection, str(entity_id)])
	# 	entity = self._get(url)
	# 	entity = map(self._validate_types, entity['entities'])
	# 	return entity[0]
	
	# def get_all(self, collection=None, sort_by='id', full=False, overload=False):
	# 	if collection is None:
	# 		collection = self.collection
	# 	if collection not in T1Object.t1_collections:
	# 		raise T1ClientError('Invalid collection.')
	# 	params = {'page_limit': 100, 'page_offset': 0, 'sort_by': sort_by}
	# 	if full is True:
	# 		params['full'] = collection[:-1]
	# 	elif isinstance(full, list):
	# 		params['full'] = ','.join(full)
	# 	url = '/'.join([self.api_base, collection])
	# 	t1_object = self._get(url, params=params)
	# 	count = t1_object['entity_count']
	# 	if count > 1000 and not overload:
	# 		print 'There are %d entities in this collection.' % count
	# 		print('Only retrieving first thousand. If you\'re sure you want all '
	# 				'of them, re-call with "overload" set to True')
	# 		for page in xrange(1, 10):
	# 			params['page_offset'] = 100*page
	# 			next_page = self._get(url, params=params)
	# 			t1_object['entities'].extend(next_page['entities'])
	# 	elif count > 100 or overload:
	# 		for page in xrange(1, int(ceil(count/100))):
	# 			params['page_offset'] = 100*page
	# 			next_page = self._get(url, params=params)
	# 			t1_object['entities'].extend(next_page['entities'])
	# 	t1_object = map(self._validate_types, t1_object['entities'])
	# 	return t1_object
	
	# def limit(self, relation, relation_id, collection=None, sort_by='id',
	# 			full=False, overload=False):
	# 	if collection is None:
	# 		collection = self.collection
	# 	if collection not in T1Object.t1_collections:
	# 		raise T1ClientError('Invalid collection.')
	# 	params = {'page_limit': 100, 'page_offset': 0, 'sort_by': sort_by}
	# 	if full is True:
	# 		params['full'] = collection[:-1]
	# 	elif isinstance(full, list):
	# 		params['full'] = ','.join(full)
	# 	relation_path = '{}={}'.format(relation, relation_id)
	# 	url = '/'.join([self.api_base, collection, 'limit', relation_path])
	# 	t1_object = self._get(url, params=params)
	# 	count = t1_object['entity_count']
	# 	if count > 1000 and not overload:
	# 		print 'There are %d entities in this collection.' % count
	# 		print('Only retrieving first thousand. If you\'re sure you want all '
	# 				'of them, re-call with "overload set to True"')
	# 		for page in xrange(1, 10):
	# 			params['page_offset'] = 100*page
	# 			next_page = self._get(url, params=params)
	# 			t1_object['entities'].extend(next_page['entities'])
	# 	elif count > 100 or overload:
	# 		for page in xrange(1, int(ceil(count/100))):
	# 			params['page_offset'] = 100*page
	# 			next_page = self._get(url, params=params)
	# 			t1_object['entities'].extend(next_page['entities'])
	# 	pass
	# 	return t1_object
	
	# def new(self, data, collection=None):
	# 	if collection is None:
	# 		collection = self.collection
	# 	if collection not in T1Object.t1_collections:
	# 		raise T1ClientError('Invalid collection.')
	# 	data = self._validate_types(data)
	# 	url = '/'.join([self.api_base, collection])
	# 	entity = self._post(url, data=data)
	# 	return entity

	# def update(self, data, collection=None):
	# 	if collection is None:
	# 		collection = self.collection
	# 	if collection not in T1Object.t1_collections:
	# 		raise T1ClientError('Invalid collection.')
	# 	if 'id' in data and not self._valid_id(data['id']):
	# 		raise T1ClientError('Cannot update object without ID! Are you trying to create?')
	# 	url = '/'.join([self.api_base, collection, str(data['id'])])
	# 	data = self._validate_types(data)
	# 	if 'version' not in data:
	# 		version = self._get(url)['entities'][0]['version']
	# 		data['version'] = int(version)
	# 	entity = self._post(url, data=data)
	# 	return entity

	def save(self, data=None):
		if self.properties.get('id'):
			url = '/'.join([self.api_base, self.collection, str(self.id)])
		else:
			url = '/'.join([self.api_base, self.collection])
		if data is not None:
			data = self._validate_write(data)
		else:
			data = self._validate_write(self.properties)
		entity = self._post(url, data=data)
		return entity

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
