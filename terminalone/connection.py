# -*- coding: utf-8 -*-
"""Provides connection object for T1.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it. Uses json and cPickle/pickle to serialize cookie objects.
"""

from __future__ import absolute_import
import warnings
from requests import Session
from .vendor.six import six
from .errors import ClientError
from .utils import PATHS
from .xmlparser import XMLParser, ParseError


class Connection(object):
	VALID_ENVS = frozenset(['production', 'qa'])
	API_BASES = {
		'production': 'api.mediamath.com',
		'qa': 't1qa2.mediamath.com',
	}
	def __init__(self,
				environment='production',
				api_base=None,
				_create_session=True,
				auth=None):
		"""Sets up Requests Session to be used for all connections to T1.

		:param environment: str to look up API Base to use. e.g. 'production'
		for https://api.mediamath.com/api/v2.0
		:param api_base: str API domain. should be the qualified domain name without
		trailing slash. e.g. "api.mediamath.com".
		:param _create_session: bool flag to create a Requests Session.
		Should only be used for initial T1 instantiation.
		"""
		if api_base is None:
			try:
				Connection.__setattr__(self, 'api_base',
						Connection.API_BASES[environment])
			except KeyError:
				raise ClientError("Environment: {!r}, does not exist.".format(environment))
		else:
			Connection.__setattr__(self, 'api_base', api_base)
		if _create_session:
			Connection.__setattr__(self, 'session', Session())

	def _check_session(self, user=None):
		if user is None:
			user, __ = self._get(PATHS['mgmt'], 'session')
		user = next(user)
		Connection.__setattr__(self, 'user_id',
							   int(user['id']))
		Connection.__setattr__(self, 'username',
							   user['name'])
		Connection.__setattr__(self, 'session_id',
							   self.session.cookies['adama_session'])

	def _get(self, path, rest, params=None):
		"""Base method for subclasses to call.
		:param path: str API path (can be from terminalone.utils.PATHS)
		:param rest: str rest of url (module-specific path, )
		:param params: dict query string params
		"""
		url = '/'.join(['https:/', self.api_base, path, rest])
		response = self.session.get(url, params=params, stream=True)

		try:
			result = XMLParser(response)
		except ParseError as e:
			Connection.__setattr__(self, 'response', response)
			raise ClientError('Could not parse XML response: {!r}'.format(e))
		except Exception:
			Connection.__setattr__(self, 'response', response)
			raise
		return iter(result.entities), result.entity_count

	def _post(self, path, rest, data):
		"""Base method for subclasses to call.
		:param url: str API URL
		:param data: dict POST data
		"""
		if not data:
			raise ClientError('No POST data.')

		url = '/'.join(['https:/', self.api_base, path, rest])
		response = self.session.post(url, data=data, stream=True)

		try:
			result = XMLParser(response)
		except ParseError as e:
			Connection.__setattr__(self, 'response', response)
			raise ClientError('Could not parse XML response: {!r}'.format(e))
		except Exception:
			Connection.__setattr__(self, 'response', response)
			raise
		return iter(result.entities), result.entity_count
