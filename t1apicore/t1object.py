# -*- coding: utf-8 -*-
"""Provides base object for T1 data classes.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import division
from datetime import datetime
from math import ceil
from sys import version_info
import t1connection
pass

class T1Object(t1connection.T1Connection):
	"""Mainly a superclass for all the various T1 Objects."""
	def __init__(self):
		super(T1Object, self).__init__()
		# dttp = datetime # DateTimeTyPe
		self.dttp = lambda ti: datetime.strptime(ti, "%Y-%m-%dT%H:%M:%S")
		self.dttf = lambda ti: datetime.strftime(ti, "%Y-%m-%dT%H:%M:%S")
		self.bool_deffalse = lambda x: x if x in frozenset(['on', 'off']) else 'off'
		self.bool_deftrue = lambda x: x if x in frozenset(['on', 'off']) else 'on'
		self.writable_attributes = {'version', 'status'} # defined for all objects
		
		self.readonly_attributes = {'id', 'build_date',' created_on',
									'updated_on', 'last_modified'}
		
		self.attribute_types = {'id': int, 'version': int, 'build_date': datetime,
			'created_on': datetime, 'updated_on': datetime, 'last_modified': datetime,
			'status': str}
		
		self.conversion_funcs = {'id': int, 'version': int, 'build_date': self.dttp,
			'created_on': self.dttp, 'updated_on': self.dttp, 'last_modified': self.dttp,
			'status': self.bool_deftrue}
		
		self.t1_collections = frozenset(['organizations', 'agencies', 'advertisers',
			'campaigns', 'strategies', 'atomic_creatives', 'concepts', 'pixel_bundles',
			'strategy_concepts', 'target_dimensions', 'reports', 'site_lists',
			'vendor_contracts', 'ad_servers', 'strategy_supply_sources',
			'strategy_day_parts'])
		# self.t1_collections_singular = frozenset([item[:-1] for item in self.t1_collections])
		pass
		# Get attribute definitions?
		# Get attribute default values?
	pass
	
	def valid_id(self, id_):
		try:
			int(id_)
		except (ValueError, TypeError):
			return False
		if id_ < 1:
			return False
		return True
	
	def get_entity_by_id(self, collection, entity_id):
		"""Wrapper for _get that enforces type.
		
		banana
		"""
		if collection not in self.t1_collections:
			raise T1Error('Invalid collection.')
		try:
			entity_id = int(entity_id)
			assert entity_id != 0
		except (ValueError, TypeError, AssertionError):
			raise T1Error('Entity called is not a valid entity ID')
		url = '/'.join([self.api_base, collection, entity_id])
		entity = self._get(url)
		pass
	
	def get_collection(self, collection, sort_by='id', full=False, overload=False):
		if collection not in self.t1_collections:
			raise T1Error('Invalid collection.')
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
					'of them, re-call with "overload=True"')
			for page in xrange(1, 10):
				params['page_offset'] = 100*page
				next_page = self._get(url, params=params)
				t1_object['entities'].extend(next_page['entities'])
		elif count > 100 or overload:
			for page in xrange(1, int(ceil(count/100))):
				params['page_offset'] = 100*page
				next_page = self._get(url, params=params)
				t1_object['entities'].extend(next_page['entities'])
		return t1_object
		pass
	
	def new_entity(self, collection, data):
		if collection not in self.t1_collections:
			raise T1Error('Invalid collection.')
		data = self.validate_types(data)
		url = '/'.join([self.api_base, collection])
		entity = self._post(url, params=data)
		return entity
	
	def update_entity(self, collection, data):
		if collection not in self.t1_collections:
			raise T1Error('Invalid collection.')
		if not self.valid_id(data['id']):
			raise T1Error('Cannot update object without ID! Are you trying to create?')
		url = '/'.join([self.api_base, collection, str(myid)])
		data = self.validate_types(data)
		if 'version' not in data:
			version = self._get(url)['entities'][0]['version']
			data['version'] = int(version)
		entity = self._post(url, params=data)
		return entity
	
	def validate_types(self, data):
		for attribute in data.copy():
			if attribute in self.readonly_attributes:
				del data[attribute]
		for key, value in data.copy().iteritems():
			if key not in self.conversion_funcs:
				raise T1Error('Unknown key: ' + key)
			proper_val = self.conversion_funcs[key](value)
			data[key] = proper_val
		return data
	
	def entity_history(self, collection, ent_id):
		if collection not in self.t1_collections:
			raise T1Error('Invalid collection.')
		if not self.valid_id(ent_id):
			raise T1Error('Valid entity ID not given')
	
	pass

