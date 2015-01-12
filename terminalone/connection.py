# -*- coding: utf-8 -*-
"""Provides connection object for T1.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it. Uses json and cPickle/pickle to serialize cookie objects.
"""

from __future__ import absolute_import
import warnings
from requests import Session
from .xmlparser import T1XMLParser, ParseError
from .errors import ClientError

class Connection(object):
	"""docstring for Connection"""
	VALID_ENVS = frozenset(['production', 'sandbox', 'demo'])
	API_BASES = {'production': 'https://api.mediamath.com/api/v2.0',
				'sandbox': 'https://t1sandbox.mediamath.com/api/v1',
				'qa': 'https://t1qa2.mediamath.com/api/v2.0',
				'demo': 'https://ewr-t1demo-n3.mediamath.com/prod/api/v1'}
	def __init__(self,
				environment='production',
				base=None, api_base=None,
				create_session=True,
				**kwargs):
		if base is None and api_base is None:
			Connection.__setattr__(self, 'api_base',
						Connection.API_BASES[environment])
		elif api_base is not None:
			Connection.__setattr__(self, 'api_base', api_base)
		else:
			warnings.warn(('`base` parameter is deprecated; use `api_base` insead.'),
						DeprecationWarning, stacklevel=2)
			Connection.__setattr__(self, 'api_base', base)
		if create_session:
			Connection.__setattr__(self, 'session', Session())

	def _get(self, url, params=None):
		"""Base method for subclasses to call."""
		response = self.session.get(url, params=params, stream=True)
		if not response.ok:
			self.response = response
			raise ClientError('Status code: {}, content: '
				'{}'.format(response.status_code, response.content))
		try:
			result = T1XMLParser(response)
		except ParseError as e:
			self.response = response
			raise ClientError('Could not parse XML response: {}'.format(e))
		return result.entities, result.entity_count
	
	def _post(self, url, data):
		"""Base method for subclasses to call."""
		if not data:
			raise ClientError('No POST data.')
		response = self.session.post(url, data=data, stream=True)
		if not response.ok:
			self.response = response
			raise ClientError('Status code: {}, content: '
				'{}'.format(response.status_code, response.content))
		try:
			result = T1XMLParser(response)
		except ParseError as e:
			self.response = response
			raise ClientError('Could not parse XML response: {}'.format(e))
		return result.entities, result.entity_count
