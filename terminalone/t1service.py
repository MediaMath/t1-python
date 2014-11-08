# -*- coding: utf-8 -*-
"""Provides service object for T1.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it. Uses json and cPickle/pickle to serialize cookie objects.
"""

# from functools import partial
from .t1connection import T1Connection
from .t1error import T1ClientError
from .t1acl import T1ACL
from .t1adserver import T1AdServer
from .t1advertiser import T1Advertiser
from .t1agency import T1Agency
from .t1atomiccreative import T1AtomicCreative
from .t1campaign import T1Campaign
from .t1concept import T1Concept
#from .t1dma import T1DMA
from .t1organization import T1Organization
from .t1permission import T1Permission
from .t1pixelbundle import T1PixelBundle
from .t1strategy import T1Strategy
from .t1targetdimension import T1TargetDimension
from .t1targetvalue import T1TargetValue
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
	'target_dimensions': T1TargetDimension,
	'target_values': T1TargetValue,
	'permissions': T1Permission,
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
	'target_dimension': T1TargetDimension,
	'target_value': T1TargetValue,
	'permission': T1Permission,
}
CHILD_PATHS = {
	'dma': 'target_dimensions/1',
	'connection speed': 'target_dimensions/2',
	'isp': 'target_dimensions/3',
	'browser': 'target_dimensions/4',
	'os': 'target_dimensions/5',
	'region': 'target_dimensions/7',
	'mathselect250': 'target_dimensions/8',
	'country': 'target_dimensions/14',
	'safety': 'target_dimensions/15',
	'channels': 'target_dimensions/16',
	'fold position': 'target_dimensions/19',
	'linear format': 'target_dimensions/20',
	'content initiation': 'target_dimensions/21',
	'audio': 'target_dimensions/22',
	'player size': 'target_dimensions/23',
	'device': 'target_dimensions/24',
	'acl': 'acl',
	'permission': 'permissions',
	'permissions': 'permissions',
}

class T1(T1Connection):
	"""Service class for ALL other T1 entities, e.g.: t1 = T1(auth)

	Accepts authentication parameters. Supports get methods to get
	collections or an entity, find method to user inner-join-like queries.
	"""
	def __init__(self, username=None, password=None, api_key=None, auth_method=None,
					environment='production', **kwargs):
		self.username = username
		self.password = password
		self.api_key = api_key
		self._authenticated = False
		self.auth = (self.username, self.password, self.api_key)
		self.environment = environment
		super(T1, self).__init__(environment, **kwargs)
		if auth_method is not None:
			self.authenticate(auth_method, **kwargs)

	# def __getattr__(self, attr):
	# 	"""Provides further active-record-like support.
	# 	Proper method is:
	# 	ac = t1.new('atomic_creatives') but this also supports
	# 	ac = t1.new_atomic_creatives() OR
	# 	ac = t1.new_atomic_creative() (because of the `self.new` behavior)
	# 	"""
	# 	if 'new_' in attr:
	# 		return partial(self.new, attr[4:])
	# 	else:
	# 		raise AttributeError(attr)

	def _check_session(self):
		self._get(self.api_base + '/session')

	def _auth_cookie(self, *args, **kwargs):
		if kwargs.get('session_id'):
			from cookielib import Cookie
			from urlparse import urlparse
			from time import time
			domain = urlparse(self.api_base).netloc
			c = Cookie(0, 'adama_session', kwargs['session_id'], None, False,
					domain, None, None, '/', True, False, int(time()+86400),
					False, None, None, {'HttpOnly':None})
			self.session.cookies.set_cookie(c)
			self._check_session()
		else:
			payload = {
				'user': self.username,
				'password': self.password,
				'api_key': self.api_key
			}
			self._post(self.api_base + '/login', data=payload)
		self._authenticated = True

	def _auth_basic(self, *args, **kwargs):
		self.session.auth = ('{}|{}'.format(self.username, self.api_key),
							self.password)
		self._check_session()
		self._authenticated = True

	def authenticate(self, auth_method, *args, **kwargs):
		if auth_method == 'cookie':
			return self._auth_cookie(*args, **kwargs)
		elif auth_method == 'basic':
			return self._auth_basic(*args, **kwargs)
		else:
			raise AttributeError('No authentication method for ' + auth_method)


	def new(self, collection, *args, **kwargs):
		"""Returns a fresh class instance for a new entity.
		t1 = T1(username, password, api_key, method="cookie")
		ac = t1.new('atomic_creative') OR
		ac = t1.new('atomic_creatives')
		"""
		try:
			ret = SINGULAR[collection]
		except KeyError:
			ret = CLASSES[collection]
		return ret(self.session, environment=self.environment,
					base=self.api_base, *args, **kwargs)

	def return_class(self, ent_dict):
		ent_type = ent_dict.get('_type', ent_dict.get('type'))
		rels = ent_dict['rels']
		if rels:
			for rel_name, data in rels.iteritems():
				ent_dict[rel_name] = self.return_class(data)
		del rels, ent_dict['rels']
		if '_acl' in ent_type:
			return T1ACL(self.session, properties=ent_dict,
							environment=self.environment)
		try:
			ret = SINGULAR[ent_type]
		except KeyError:
			ret = CLASSES[ent_type]
		return ret(self.session, properties=ent_dict,
					environment=self.environment)

	def get(self, collection,
			entity=None,
			child=None,
			limit=None,
			include=None,
			full=None,
			page_limit=100,
			page_offset=0,
			sort_by='id',
			count=False):
		url = [self.api_base, collection]
		if entity is not None:
			url.append(str(entity)) # str so that we can use join
			params = {}
		else:
			params = {'page_limit': page_limit, 'page_offset': page_offset,
						'sort_by': sort_by}
		if child is not None:
			try:
				url.append(CHILD_PATHS[child.lower()])
			except AttributeError:
				raise T1ClientError("child must be a string corresponding to the entity retrieved")
			except KeyError:
				raise T1ClientError("Attempted to retrieve an entity not in T1")
		if isinstance(limit, dict):
			if len(limit) != 1:
				raise T1ClientError('Limit must consist of one parent collection'
					' (or chained parent collection) and a single value for it'
					' (e.g. {"advertiser": 1}, or {"advertiser.agency": 2)')
			url.extend(['limit', '{0!s}={1:d}'.format(*limit.items()[0])])
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
		if entity is not None:
			if child is not None:
				entities[0]['id'] = url.split('/')[-1]
				entities[0]['parent_id'] = entity
				entities[0]['parent'] = collection
			return self.return_class(entities[0])
		for index, entity in enumerate(entities):
			entities[index] = self.return_class(entity)
		if count:
			return entities, ent_count
		else:
			return entities
	def get_all(*args, **kwargs):
		first_pg, count = self.get(*args, **kwargs)
		pass # TODO finish implementing iterating over pages

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
			url.extend(['limit', '{0!s}={1:d}'.format(*limit.items()[0])])
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
		params = {'q': '{}=:{}'.format(key, query)}
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

T1Service = T1
