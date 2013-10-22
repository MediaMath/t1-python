# -*- coding: utf-8 -*-
"""Provides connection object for T1.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it. Uses json and cPickle/pickle to serialize cookie objects.
"""

# import contextlib
# import json
from os.path import getsize, isfile, realpath, dirname
from time import time
import requests
from .xmlparser import T1XMLParser

CURRENT_DIR = dirname(realpath(__file__))
# T1_API_ENV = 'production'


# def _load_config(configfile):
# 	required_config_fields = frozenset(['username', 'password', 'base_uri'])
# 	with open(configfile) as f:
# 		config = json.load(f)
# 	for field in required_config_fields:
# 		if field not in config:
# 			raise T1LoginException('Invalid config')
# 	return config

class T1Connection(object):
	"""docstring for T1Connection"""
	VALID_ENVS = frozenset(['production', 'sandbox', 'demo'])
	API_BASES = {'production': 'https://api.mediamath.com/api/v1',
				'sandbox': 'https://t1sandbox.mediamath.com/api/v1',
				'demo': 'https://ewr-t1demo-n3.mediamath.com/prod/api/v1'}
	def __init__(self, auth, environment='production', base=None):
		if base is None:
			T1Connection.__setattr__(self, 'api_base',
						T1Connection.API_BASES[environment])
			# self.api_base = self.API_BASES[environment]
		else:
			T1Connection.__setattr__(self, 'api_base', base)
			# self.api_base = base
		T1Connection.__setattr__(self, 'adama', requests.Session())
		self.adama.__setattr__('auth', auth)

	def _get(self, url, params=None):
		"""Base method for subclasses to call."""
		try:
			response = self.adama.get(url, params=params, stream=True)
			result = T1XMLParser(response.raw)
		except T1AuthRequiredError as e:
			print('Your T1 credentials appear to be incorrect. '
					'Please check your configuration.')
			raise
		return result.entities, result.entity_count
	
	def _post(self, url, data):
		"""Base method for subclasses to call."""
		if not data:
			raise T1ClientError('No POST data.')
		try:
			response = self.adama.post(url, data=data,
							stream=True)
			result = T1XMLParser(response.raw)
		except T1AuthRequiredError as e:
			print('Your T1 credentials appear to be incorrect. '
					'Please check your configuration.')
			raise
		return result.entities, result.entity_count
	pass
