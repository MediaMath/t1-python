# -*- coding: utf-8 -*-
"""Provides service object for T1.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it. Uses json and cPickle/pickle to serialize cookie objects.
"""

from functools import partial
from .t1connection import T1Connection
from .t1error import T1ClientError
from .t1adserver import T1AdServer
from .t1advertiser import T1Advertiser
from .t1agency import T1Agency
from .t1atomiccreative import T1AtomicCreative
from .t1campaign import T1Campaign
from .t1concept import T1Concept
from .t1organization import T1Organization
from .t1pixelbundle import T1PixelBundle
from .t1strategy import T1Strategy
from .t1user import T1User

CLASSES = {
	'ad_servers': T1AdServer,
	'advertisers': T1Advertiser,
	'agencies': T1Agency,
	'atomic_creatives': T1AtomicCreative,
	'campaigns': T1Campaign,
	'concepts': T1Concept,
	'organizations': T1Organization,
	# 'pixels': T1Pixel,
	'pixel_bundles': T1PixelBundle,
	'strategies': T1Strategy,
	'users': T1User,
	
}
SINGULAR = {
	'ad_server': T1AdServer,
	'advertiser': T1Advertiser,
	'agency': T1Agency,
	'atomic_creative': T1AtomicCreative,
	'campaign': T1Campaign,
	'concept': T1Concept,
	'organization': T1Organization,
	# 'pixel': T1Pixel,
	'pixel_bundle': T1PixelBundle,
	'strategy': T1Strategy,
	'user': T1User,
}

class T1Service(T1Connection):
	"""Service class for ALL other T1 entities, e.g.: t1 = T1Service(auth)
	
	Accepts authentication parameters.Supports get methods to get
	collections or an entity, find method to user inner-join-like queries.
	"""
	def __init__(self, username, password, apikey=None,
					environment='production'):
		self.password = password
		if apikey is not None:
			self.username = '{}|{}'.format(username, apikey)
		else:
			self.username = username
		auth = (self.username, self.password)
		super(T1Service, self).__init__(auth, environment)
		self._check_session()
		# self.adama.auth = (self.username, self.password)
	def __getattr__(self, attr):
		"""Provides further active-record-like support.
		Proper method is:
		ac = t1.new('atomic_creatives') BUT ALSO SUPPORTS
		ac = t1.new_atomic_creatives() OR
		ac = t1.new_atomic_creative() (because of the `new` behavior)
		"""
		if 'new_' in attr:
			attr = attr[4:]
			return partial(self.new, attr)
		else:
			raise AttributeError

	def _check_session(self):
		self._get(self.api_base + '/session')

	# @classmethod # Because we need auth here, can't be class method
	# def new(cls, collection):
	def new(self, collection):
		"""Returns a fresh class instance for a new entity.
		t1 = T1Service(auth)
		ac = t1.new('atomic_creatives') OR
		ac = t1.new('atomic_creative')
		Provides KeyError support for singular entity. Recommended is
		to use the proper plural collection name.
		"""
		try:
			return CLASSES[collection](self.adama.auth)
		except KeyError:
			return SINGULAR[collection](self.adama.auth)

	def return_class(self, ent_dict):
		ent_type = ent_dict.get('_type', ent_dict.get('type'))
		rels = ent_dict['rels']
		if rels:
			for rel_name, data in rels.iteritems():
				ent_dict[rel_name] = self.return_class(data)
		del rels, ent_dict['rels']
		try:
			return SINGULAR[ent_type](self.adama.auth, properties=ent_dict)
		except KeyError:
			return CLASSES[ent_type](self.adama.auth, properties=ent_dict)

	def get(self, collection, entity=None, limit=None,
			include=None, full=None, sort_by='id',
			page_offset=0, page_limit=100, count=False):
		url = [self.api_base, collection]
		if entity is not None:
			url.append(str(entity)) # str so that we can use join
			params = {}
		else:
			params = {'page_limit': page_limit, 'page_offset': page_offset,
						'sort_by': sort_by}
		if isinstance(limit, dict):
			if len(limit) != 1:
				raise T1ClientError('Limit must consist of one parent collection'
					' (or chained parent collection) and a single value for it'
					' (e.g. {"advertiser": 1}, or {"advertiser.agency": 2)')
			url.extend(['limit', '{0!s}={1!d}'.format(*limit.items()[0])])
		if isinstance(include, list): # Can't use "with" here because keyword
			params['with'] = ','.join(include)
		elif include is not None:
			params['with'] = include
		if isinstance(full, list):
			params['full'] = ','.join(full)
		elif full is not None:
			params['full'] = full
		url = '/'.join(url)
		entities, ent_count = self._get(url, params=params)
		if entity:
			return self.return_class(entities[0])
		for index, entity in enumerate(entities):
			entities[index] = self.return_class(entity)
		if count:
			return entities, ent_count
		else:
			return entities

	def __get_all(self, collection, limit=None,
				include=None, full=None, sort_by='id', count=False):
		"""Retrieves all records for a collection or limited collection.
		
		ONLY INCLUDED FOR COMPLETENESS. Normally self.get should be used, as
		T1 will soon reject queries without a page_limit parameter.
		"""
		url = [self.api_base, collection]
		params = {'sort_by': sort_by}
		if isinstance(limit, dict):
			if len(limit) != 1:
				raise T1ClientError('Limit must consist of one parent collection'
					' (or chained parent collection) and a single value for it'
					' (e.g. {"advertiser": 1}, or {"advertiser.agency": 2)')
			url.extend(['limit', '{0!s}={1!d}'.format(*limit.items()[0])])
		if isinstance(include, list): # Can't use "with" here because keyword
			params['with'] = ','.join(include)
		elif include is not None:
			params['with'] = include
		if isinstance(full, list):
			params['full'] = ','.join(full)
		elif full is not None:
			params['full'] = full
		url = '/'.join(url)
		entities = self._get(url, params=params)
		for index, entity in enumerate(entities):
			entities[index] = self.return_class(entity)
		return entities
	
	def get_sub(self, collection, entity, sub, *args):
		pass

	def find(self, collection, key, query, full=None, count=False):
		url = '/'.join([self.api_base, collection])
		params = {'q': '{}%3D%3A{}'.format(key, query)}
		if isinstance(full, list):
			params['full'] = ','.join(full)
		elif full is not None:
			params['full'] = full
		entities, ent_count = self._get(url, params=params)
		for index, entity in enumerate(entities):
			entities[index] = self.return_class(entity)
		if count:
			return entities, ent_count
		else:
			return entities
