# -*- coding: utf-8 -*-
"""Provides service object for T1.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it. Uses json and cPickle/pickle to serialize cookie objects.
"""

from functools import partial
from .t1connection import T1Connection
from .t1atomiccreative import T1AtomicCreative
from .t1advertiser import T1Advertiser
from .t1agency import T1Agency
from .t1campaign import T1Campaign
from .t1concept import T1Concept
from .t1organization import T1Organization
from .t1pixelbundle import T1PixelBundle
from .t1strategy import T1Strategy
from .t1user import T1User

CLASSES = {
	'atomic_creatives': T1AtomicCreative,
	'pixel_bundles': T1PixelBundle,
	'advertisers': T1Advertiser,
	'agencies': T1Agency,
	'organizations': T1Organization,
	'campaigns': T1Campaign,
	'strategies': T1Strategy,
	'concepts': T1Concept,
	# 'pixels': T1Pixel,
	'users': T1User,
	
}
SINGULAR = {
	'atomic_creative': T1AtomicCreative,
	'pixel_bundle': T1PixelBundle,
	'advertiser': T1Advertiser,
	'agency': T1Agency,
	'organization': T1Organization,
	'campaign': T1Campaign,
	'strategy': T1Strategy,
	'concept': T1Concept,
	# 'pixel': T1Pixel,
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
		ent_type = ent_dict.get('_type', ent_dict['type'])
		parent = ent_dict.get('parent')
		if parent:
			ent_dict['parent'] = self.return_class(parent)
		try:
			return SINGULAR[ent_type](self.adama.auth, properties=ent_dict)
		except KeyError:
			return CLASSES[ent_type](self.adama.auth, properties=ent_dict)

	def get(self, collection, entity=None, limit=None,
			inc=None, full=None, sort_by='id', page_offset=0, count=False):
		url = [self.api_base, collection]
		clas = CLASSES[collection]
		if entity is not None:
			url.append(str(entity))
			params = {}
		else:
			params = {'page_limit': 100, 'page_offset': page_offset,
						'sort_by': sort_by}
		if isinstance(limit, dict):
			url.extend(['limit', '%s=%d' % limit.popitem()])
		# if isinstance(inc, list): # NOT YET IMPLEMENTED
		# 	params['with'] = ','.join(inc)
		# elif inc is not None:
		# 	params['with'] = inc
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
				inc=None, full=None, sort_by='id', count=False):
		"""Retrieves all records for a collection or limited collection.
		
		ONLY INCLUDED FOR COMPLETENESS. Normally self.get should be used, as
		T1 will soon reject queries without a page_limit parameter.
		"""
		url = [self.api_base, collection]
		clas = CLASSES[collection]
		params = {'sort_by': sort_by}
		if isinstance(limit, dict):
			url.extend(['limit', '%s=%d' % limit.popitem()])
		# if isinstance(inc, list): # NOT YET IMPLEMENTED
		# 	params['with'] = ','.join(inc)
		# elif inc is not None:
		# 	params['with'] = inc
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
		clas = CLASSES[collection]
		entities, ent_count = self._get(url, params=params)
		for index, entity in enumerate(entities):
			entities[index] = self.return_class(entity)
		if count:
			return entities, ent_count
		else:
			return entities
