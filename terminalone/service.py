# -*- coding: utf-8 -*-
"""Provides service object for T1.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it. Uses json and cPickle/pickle to serialize cookie objects.
"""

from __future__ import absolute_import, division
# from functools import partial
from .connection import Connection
from .constants import filters
from .errors import ClientError
from .models.acl import ACL
from .models.adserver import AdServer
from .models.advertiser import Advertiser
from .models.agency import Agency
from .models.atomiccreative import AtomicCreative
from .models.campaign import Campaign
from .models.concept import Concept
from .models.organization import Organization
from .models.permission import Permission
from .models.pixelbundle import PixelBundle
from .models.strategy import Strategy
from .models.targetdimension import TargetDimension
from .models.targetvalue import TargetValue
from .models.user import User
from .vendor.six import six

CLASSES = {
	'ad_servers': AdServer,
	'advertisers': Advertiser,
	'agencies': Agency,
	'atomic_creatives': AtomicCreative,
	'campaigns': Campaign,
	'concepts': Concept,
	'organizations': Organization,
	# 'pixels': Pixel,
	'pixel_bundles': PixelBundle,
	'strategies': Strategy,
	'users': User,
	'target_dimensions': TargetDimension,
	'target_values': TargetValue,
	'permissions': Permission,
}
SINGULAR = {
	'ad_server': AdServer,
	'advertiser': Advertiser,
	'agency': Agency,
	'atomic_creative': AtomicCreative,
	'campaign': Campaign,
	'concept': Concept,
	'organization': Organization,
	# 'pixel': Pixel,
	'pixel_bundle': PixelBundle,
	'strategy': Strategy,
	'user': User,
	'target_dimension': TargetDimension,
	'target_value': TargetValue,
	'permission': Permission,
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

class T1(Connection):
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
			if '_acl' in collection:
				ret = ACL
			else:
				ret = CLASSES[collection]
		return ret(self.session,
					environment=self.environment,
					base=self.api_base,
					*args, **kwargs)

	def return_class(self, ent_dict):
		ent_type = ent_dict.get('_type', ent_dict.get('type'))
		rels = ent_dict['rels']
		if rels:
			for rel_name, data in six.iteritems(rels):
				ent_dict[rel_name] = self.return_class(data)
		del rels, ent_dict['rels']
		return self.new(ent_type, properties=ent_dict)

	def _gen_classes(self, entities):
		for entity in entities:
			yield self.return_class(entity)

	def _construct_params(self, entity, include, full, page_limit,
						page_offset, sort_by, query):
		if entity is not None:
			params = {}
		else:
			params = {'page_limit': page_limit,
						'page_offset': page_offset,
						'sort_by': sort_by,
						'q': query,}
		if isinstance(include, list): # Can't use "with" here because keyword
			params['with'] = ','.join(include)
		elif include is not None:
			params['with'] = include
		if isinstance(full, list):
			params['full'] = ','.join(full)
		elif full is True:
			params['full'] = '*'
		elif full is not None:
			params['full'] = full
		return params

	def _construct_url(self, collection, entity, child, limit):
		url = [self.api_base, collection]
		if entity is not None:
			url.append(str(entity)) # str so that we can use join

		if child is not None:
			try:
				url.append(CHILD_PATHS[child.lower()])
			except AttributeError:
				raise ClientError("Child must be a string corresponding to the entity retrieved")
			except KeyError:
				raise ClientError("Attempted to retrieve an entity not in T1")

		if isinstance(limit, dict):
			if len(limit) != 1:
				raise ClientError('Limit must consist of one parent collection'
					' (or chained parent collection) and a single value for it'
					' (e.g. {"advertiser": 1}, or {"advertiser.agency": 2)')
			url.extend(['limit',
						'{0!s}={1:d}'.format(*six.advance_iterator(six.iteritems(limit)))])

		return '/'.join(url)

	def get(
		self,
		collection,
		entity=None,
		child=None,
		limit=None,
		include=None,
		full=None,
		page_limit=100,
		page_offset=0,
		sort_by='id',
		get_all=False,
		query=None,
		count=False,
		_url=None,
		_params=None
	):
		if page_limit > 100:
			raise ClientError('page_limit parameter must not exceed 100')

		if _url is None:
			_url = self._construct_url(collection, entity, child, limit)

		if get_all:
			gen = self._get_all(collection,
						entity=entity,
						child=child,
						include=include,
						full=full,
						sort_by=sort_by,
						query=query,
						count=count,
						_url=_url)
			if count:
				ent_count = next(gen)
				return gen, ent_count
			else:
				return gen

		if _params is None:
			_params = self._construct_params(entity, include, full, page_limit,
										page_offset, sort_by, query)

		entities, ent_count = self._get(_url, params=_params)
		if entity is not None:
			entities = six.advance_iterator(iter(entities))
			if child is not None:
				entities['id'] = url.split('/')[-1]
				entities['parent_id'] = entity
				entities['parent'] = collection
			return self.return_class(entities)

		ent_gen = self._gen_classes(entities)
		if count:
			return ent_gen, ent_count
		else:
			return ent_gen

	def get_all(self, collection, **kwargs):
		"""Retrieves all entities in a collection. Has same signature as .get."""
		if 'get_all' in kwargs:
			del kwargs['get_all']
		return self.get(collection, get_all=True, **kwargs)

	def _get_all(self, collection, **kwargs):
		_, num_recs = self._get(kwargs['_url'], params={
			'page_limit': 1,
			'q': kwargs.get('query'),
		})

		if kwargs.get('count'):
			yield num_recs

		for page_offset in six.moves.range(0, num_recs, 100):
			gen = self.get(collection,
							_url=kwargs['_url'],
							entity=kwargs.get('entity'),
							include=kwargs.get('include'),
							full=kwargs.get('full'),
							page_offset=page_offset,
							sort_by=kwargs.get('sort_by'),
							query=kwargs.get('query'))
			for item in gen:
				yield item

	# def get_sub(self, collection, entity, sub, *args):
	# 	pass

	def find(self, collection, variable, operator, candidates, **kwargs):
		if operator == filters.IN:
			if not isinstance(candidates, list):
				raise ClientError('candidates must be list of entities for operator IN')
			q = '(' + ','.join(str(c) for c in candidates) + ')'
		else:
			q = operator.join([variable, str(candidates or 'null')])
		return self.get(collection, query=q, **kwargs)

T1Service = T1
