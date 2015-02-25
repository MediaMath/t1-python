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
from .xmlparser import T1XMLParser, ParseError


class Connection(object):
	VALID_ENVS = frozenset(['production', 'sandbox', 'qa', 'demo'])
	API_BASES = {
		'production': 'https://api.mediamath.com/api/v2.0',
		'sandbox': 'https://t1sandbox.mediamath.com/api/v1',
		'qa': 'https://t1qa2.mediamath.com/api/v2.0',
		'demo': 'https://ewr-t1demo-n3.mediamath.com/prod/api/v1'
	}
	def __init__(self,
				environment='production',
				base=None, api_base=None,
				create_session=True,
				auth=None):
		"""Sets up Requests Session to be used for all connections to T1.

		:param environment: str to look up API Base to use. e.g. 'production'
		for https://api.mediamath.com/api/v2.0
		:param base: str API base. should be in format https://[url] without
		trailing slash, and including version. Will be deprecated.
		:param api_base: str alias for base. Preferred.
		:param create_session: bool flag to create a Requests Session.
		Should only be used for initial T1 instantiation.
		"""
		if base is None and api_base is None:
			try:
				Connection.__setattr__(self, 'api_base',
						Connection.API_BASES[environment])
			except KeyError:
				raise ClientError("Environment: {!r}, does not exist.".format(environment))
		elif api_base is not None:
			Connection.__setattr__(self, 'api_base', api_base)
		else:
			warnings.warn('`base` parameter is deprecated; use `api_base` instead.',
						DeprecationWarning, stacklevel=2)
			Connection.__setattr__(self, 'api_base', base)
		if create_session:
			Connection.__setattr__(self, 'session', Session())

	def _check_session(self):
		user, _ = self._get(self.api_base + '/session')
		Connection.__setattr__(self, 'user_id',
							   int(six.advance_iterator(iter(user))['id']))
		Connection.__setattr__(self, 'session_id',
							   self.session.cookies['adama_session'])

	def _get(self, url, params=None):
		"""Base method for subclasses to call.
		:param url: str API URL
		:param params: dict query string params
		"""
		response = self.session.get(url, params=params, stream=True)

		try:
			result = T1XMLParser(response)
		except ParseError as e:
			self.response = response
			raise ClientError('Could not parse XML response: {!r}'.format(e))
		return result.entities, result.entity_count

	def _post(self, url, data):
		"""Base method for subclasses to call.
		:param url: str API URL
		:param data: dict POST data
		"""
		if not data:
			raise ClientError('No POST data.')
		response = self.session.post(url, data=data, stream=True)

		try:
			result = T1XMLParser(response)
		except ParseError as e:
			self.response = response
			raise ClientError('Could not parse XML response: {!r}'.format(e))
		return result.entities, result.entity_count
