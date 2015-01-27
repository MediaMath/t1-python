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
from .entity import Entity
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
	def __init__(self,
				 username=None,
				 password=None,
				 api_key=None,
				 auth_method=None,
				 session_id=None,
				 environment='production',
				 api_base=None,
				 **kwargs):
		"""Set up session for main service object.

		:param username: str T1 Username
		:param password: str T1 Password
		:param api_key: str API Key approved in Developer Portal
		:param session_id: str API-provided prior session cookie.
		For instance, if you have a session ID provided by browser cookie,
		you can use that to authenticate a server-side connection.
		:param auth_method: enum('cookie', 'basic') Method for authentication.
		:param environment: str to look up API Base to use. e.g. 'production'
		for https://api.mediamath.com/api/v2.0
		:param api_base: str API base. should be in format https://[url] without
		trailing slash, and including version.
		"""
		self.username = username
		self.password = password
		self.api_key = api_key
		self._authenticated = False
		self._auth = (self.username, self.password, self.api_key)
		self.environment = environment
		super(T1, self).__init__(environment, api_base=api_base, **kwargs)
		if auth_method is not None:
			self.authenticate(auth_method, session_id=session_id, **kwargs)

	def _auth_cookie(self, session_id=None, **kwargs):
		if session_id is not None:
			from time import time
			self.session.cookies.set(
				name='adama_session',
				value=session_id,
				domain=six.moves.urllib.parse.urlparse(self.api_base).netloc,
				expires=kwargs.get('expires', int(time()+86400)),
			)
			self._check_session()
		else:
			payload = {
				'user': self.username,
				'password': self.password,
				'api_key': self.api_key
			}
			self._post(self.api_base + '/login', data=payload)
		self._authenticated = True

	def _auth_basic(self):
		self.session.auth = ('{}|{}'.format(self.username, self.api_key),
							self.password)
		self._check_session()
		self._authenticated = True

	def authenticate(self, auth_method, **kwargs):
		if auth_method == 'cookie':
			return self._auth_cookie(**kwargs)
		elif auth_method == 'basic':
			return self._auth_basic()
		else:
			raise AttributeError('No authentication method for ' + auth_method)


	def new(self, collection, *args, **kwargs):
		"""Returns a fresh class instance for a new entity.

		ac = t1.new('atomic_creative') OR
		ac = t1.new('atomic_creatives')
		"""
		if isinstance(collection, Entity):
			ret = collection
		elif '_acl' in collection:
			ret = ACL
		else:
			try:
				ret = SINGULAR[collection]
			except KeyError:
				ret = CLASSES[collection]
		return ret(self.session,
					environment=self.environment,
					base=self.api_base,
					auth=self._auth,
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

	@staticmethod
	def _construct_params(entity, include, full, page_limit,
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
				raise ClientError("`child` must be a string of the entity to retrieve")
			except KeyError:
				raise ClientError("`child` must correspond to an entity not in T1")

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
		"""Main retrieval method for T1 Entities.

		:param collection: str T1 collection, e.g. "advertisers", "organizations"
		:param entity: int ID of entity being retrieved from T1
		:param child: str child, e.g. "dma", "acl"
		:param limit: dict[str]int query for relation entity, e.g. {"advertiser": 123456}
		:param include: str/list of relations to include, e.g. "advertiser", ["campaign", "advertiser"]
		:param full: str/bool which entities to return
		:param page_limit: int number of entities to return per query, 100 max
		:param page_offset: int offset for results returned.
		:param sort_by: str sort order. Default "id". e.g. "-id", "name"
		:param get_all: bool whether to retrieve all results for a query or just a single page
		:param query: str search parameter. Invoked by `find`
		:param count: bool return the number of entities as a second parameter
		:param _url: str shortcut to bypass URL determination.
		:param _params: dict query string parameters to bypass query determination
		:return: If:
			Collection is requested => generator over collection of entity objects
			Entity ID is provided => Entity object
			`count` is True => number of entities as second return val
		:raise ClientError: if page_limit > 100
		"""
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
				entities['id'] = _url.split('/')[-1]
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
		kwargs.pop('get_all', None)
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
				raise ClientError('`candidates` must be list of entities for `IN`')
			q = '(' + ','.join(str(c) for c in candidates) + ')'
		else:
			q = operator.join([variable, str(candidates or 'null')])
		return self.get(collection, query=q, **kwargs)

T1Service = T1
