# -*- coding: utf-8 -*-
"""Provides base object for T1 data classes.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import division, absolute_import
from datetime import datetime
from math import ceil
from t1connection import *
pass

class T1Object(T1Connection):
	"""Mainly a superclass for all the various T1 Objects."""
	t1_collections = frozenset(['organizations', 'agencies', 'advertisers',
			'campaigns', 'strategies', 'atomic_creatives', 'concepts', 'pixel_bundles',
			'strategy_concepts', 'target_dimensions', 'reports', 'site_lists',
			'vendor_contracts', 'ad_servers', 'strategy_supply_sources',
			'strategy_day_parts', 'users'])
	def __init__(self):
		super(T1Object, self).__init__()
		# dttp = datetime # DateTimeTyPe
		self.collection = None
		self._writable = {'version', 'status'} # defined for all objects
		
		self._readonly = {'id', 'build_date',' created_on', 'type',
							'updated_on', 'last_modified'}
		
		self._types = {'id': int, 'version': int, 'build_date': datetime,
			'created_on': datetime, 'updated_on': datetime, 'last_modified': datetime,
			'status': str, 'name': str}
		
		self._convert = {'id': int, 'version': int, 'build_date': self._strpt,
			'created_on': self._strpt, 'updated_on': self._strpt, 'last_modified': self._strpt,
			'status': self._bool_deftrue, 'name': str}
		
		pass
		# Get attribute definitions?
		# Get attribute default values?
	pass
	
	def _strpt(self, ti):
		return datetime.strptime(ti, "%Y-%m-%dT%H:%M:%S")
	
	def _strft(self, ti):
		return datetime.strftime(ti, "%Y-%m-%dT%H:%M:%S")
	
	def _bool_deffalse(self, x, comp=frozenset(['on', 'off'])):
		if x in comp:
			return x
		return 'off'
	def _bool_deftrue(self, x, comp=frozenset(['on', 'off'])):
		if x in comp:
			return x
		return 'on'
	
	def _valid_id(self, id_):
		try:
			int(id_)
		except (ValueError, TypeError):
			return False
		if id_ < 1:
			return False
		return True
	
	def _validate_types(self, data):
		for attribute in data.copy():
			if attribute in self._readonly:
				del data[attribute]
		for key, value in data.copy().iteritems():
			if key not in self._convert:
				raise T1ClientError('Unknown key: ' + key)
			proper_val = self._convert[key](value)
			data[key] = proper_val
		return data
	
	def get_one(self, entity_id, collection=None):
		"""Wrapper for _get that enforces type.
		
		banana
		"""
		if collection is None:
			collection = self.collection
		if collection not in T1Object.t1_collections:
			raise T1ClientError('Invalid collection.')
		try:
			entity_id = int(entity_id)
			assert entity_id != 0
		except (ValueError, TypeError, AssertionError):
			raise T1ClientError('Entity called is not a valid entity ID')
		url = '/'.join([self.api_base, collection, entity_id])
		entity = self._get(url)
		pass
		return entity
	
	def get_all(self, collection=None, sort_by='id', full=False, overload=False):
		if collection is None:
			collection = self.collection
		if collection not in T1Object.t1_collections:
			raise T1ClientError('Invalid collection.')
		params = {'page_limit': 100, 'page_offset': 0, 'sort_by': sort_by}
		if full is True:
			params['full'] = collection[:-1]
		elif isinstance(full, list):
			params['full'] = ','.join(full)
		url = '/'.join([self.api_base, collection])
		t1_object = self._get(url, params=params)
		count = t1_object['entity_count']
		if count > 1000 and not overload:
			print 'There are %d entities in this collection.' % count
			print('Only retrieving first thousand. If you\'re sure you want all '
					'of them, re-call with "overload set to True"')
			for page in xrange(1, 10):
				params['page_offset'] = 100*page
				next_page = self._get(url, params=params)
				t1_object['entities'].extend(next_page['entities'])
		elif count > 100 or overload:
			for page in xrange(1, int(ceil(count/100))):
				params['page_offset'] = 100*page
				next_page = self._get(url, params=params)
				t1_object['entities'].extend(next_page['entities'])
		pass
		return t1_object
	
	def limit(self, relation, relation_id, collection=None, sort_by='id',
				full=False, overload=False):
		if collection is None:
			collection = self.collection
		if collection not in T1Object.t1_collections:
			raise T1ClientError('Invalid collection.')
		params = {'page_limit': 100, 'page_offset': 0, 'sort_by': sort_by}
		if full is True:
			params['full'] = collection[:-1]
		elif isinstance(full, list):
			params['full'] = ','.join(full)
		relation_path = '{}={}'.format(relation, relation_id)
		url = '/'.join([self.api_base, collection, 'limit', relation_path])
		t1_object = self._get(url, params=params)
		count = t1_object['entity_count']
		if count > 1000 and not overload:
			print 'There are %d entities in this collection.' % count
			print('Only retrieving first thousand. If you\'re sure you want all '
					'of them, re-call with "overload set to True"')
			for page in xrange(1, 10):
				params['page_offset'] = 100*page
				next_page = self._get(url, params=params)
				t1_object['entities'].extend(next_page['entities'])
		elif count > 100 or overload:
			for page in xrange(1, int(ceil(count/100))):
				params['page_offset'] = 100*page
				next_page = self._get(url, params=params)
				t1_object['entities'].extend(next_page['entities'])
		pass
		return t1_object
	
	def new(self, data, collection=None):
		if collection is None:
			collection = self.collection
		if collection not in T1Object.t1_collections:
			raise T1ClientError('Invalid collection.')
		data = self._validate_types(data)
		url = '/'.join([self.api_base, collection])
		entity = self._post(url, params=data)
		return entity
	
	def update(self, data, collection=None):
		if collection is None:
			collection = self.collection
		if collection not in T1Object.t1_collections:
			raise T1ClientError('Invalid collection.')
		if not self._valid_id(data['id']):
			raise T1ClientError('Cannot update object without ID! Are you trying to create?')
		url = '/'.join([self.api_base, collection, int(data['id'])])
		data = self._validate_types(data)
		if 'version' not in data:
			version = self._get(url)['entities'][0]['version']
			data['version'] = int(version)
		entity = self._post(url, params=data)
		return entity
	
	def history(self, ent_id, collection=None):
		if collection is None:
			collection = self.collection
		if collection not in T1Object.t1_collections:
			raise T1ClientError('Invalid collection.')
		if not self._valid_id(ent_id):
			raise T1ClientError('Valid entity ID not given')
		url  = '/'.join([self.api_base, collection, str(ent_id), 'history'])
		history = self._get(url)
		return history
	
	pass
