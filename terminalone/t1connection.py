# -*- coding: utf-8 -*-
"""Provides connection object for T1.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it. Uses json and cPickle/pickle to serialize cookie objects.
"""

from os.path import getsize, isfile, realpath, dirname
from time import time
import requests
from .xmlparser import T1XMLParser, ParseError
from .t1error import T1ClientError

class T1Connection(object):
	"""docstring for T1Connection"""
	VALID_ENVS = frozenset(['production', 'sandbox', 'demo'])
	API_BASES = {'production': 'https://api.mediamath.com/api/v1',
				'sandbox': 'https://t1sandbox.mediamath.com/api/v1',
				'demo': 'https://ewr-t1demo-n3.mediamath.com/prod/api/v1'}
	def __init__(self, environment='production', base=None,
				create_session=True, **kwargs):
		if base is None:
			T1Connection.__setattr__(self, 'api_base',
						T1Connection.API_BASES[environment])
		else:
			T1Connection.__setattr__(self, 'api_base', base)
		if create_session:
			T1Connection.__setattr__(self, 'session', requests.Session())

	def _get(self, url, params=None):
		"""Base method for subclasses to call."""
		response = self.session.get(url, params=params, stream=True)
		if not response.ok:
			self.response = response
			raise T1ClientError('Status code: {}, content: '
				'{}'.format(response.status_code, response.content))
		try:
			result = T1XMLParser(response)
		except ParseError as e:
			self.response = response
			raise T1ClientError('Could not parse XML response: {}'.format(e))
		return result.entities, result.entity_count
	
	def _post(self, url, data):
		"""Base method for subclasses to call."""
		if not data:
			raise T1ClientError('No POST data.')
		response = self.session.post(url, data=data, stream=True)
		if not response.ok:
			self.response = response
			raise T1ClientError('Status code: {}, content: '
				'{}'.format(response.status_code, response.content))
		try:
			result = T1XMLParser(response)
		except ParseError as e:
			self.response = response
			raise T1ClientError('Could not parse XML response: {}'.format(e))
		return result.entities, result.entity_count
