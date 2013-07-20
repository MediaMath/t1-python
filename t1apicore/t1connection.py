# -*- coding: utf-8 -*-
"""Provides connection object for T1.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it. Uses json and cPickle/pickle to serialize cookie objects.
"""

# import contextlib
import json
from os.path import getsize, isfile
from time import time
try:
	import cPickle as pickle
except ImportError:
	import pickle
import requests
from requests.utils import dict_from_cookiejar, cookiejar_from_dict
from xmlparser import *

# API_BASE = 'https://t1.mediamath.com/api/v1/'
# T1_API_ENV = 'production'

# xmlparser imports t1error so don't want to import it here too

class T1Connection(object):
	"""docstring for T1Connection"""
	VALID_ENVS = frozenset(['production', 'sandbox'])
	def __init__(self, environment='production'):
		self.config = self.load_config('t1api.{}.json'.format(environment if environment 
															in T1Connection.VALID_ENVS else 'sandbox'))
		# super(T1Connection, self).__init__()
		self.t1nowtime = lambda: int(time())
		self.adama_session = requests.Session()
		self.api_base = 'https://' + self.config['base_uri']
		if self.config.get('api_key'):
			authuser = '{}|{}'.format(self.config['username'], self.config['api_key'])
		else:
			authuser = self.config['username']
		self.auth = (authuser, self.config['password'])
	
	def load_config(self, configfile):
		required_config_fields = frozenset(['username', 'password', 'base_uri',
											'cookie_path'])
		with open(configfile) as f:
			config = json.load(f)
		for field in required_config_fields:
			if field not in config:
				raise T1LoginException('Invalid config')
		return config

	def _get(self, url, params=None):
		"""Base method for subclasses to call."""
		try:
			response = self.adama_session.get(url, params=params,
							auth=self.auth, stream=True)
			result = T1XMLParser(response.raw)
		except T1AuthRequiredError as e:
			print('Your T1 credentials appear to be incorrect. '
					'Please check your configuration.')
			raise
		pass
		return result.attribs
	
	def _post(self, url, data):
		"""Base method for subclasses to call."""
		if not data:
			raise T1ClientError('No POST data.')
		try:
			response = self.adama_session.post(url, data=data,
							auth=self.auth, stream=True)
			result = T1XMLParser(response.raw)
		except T1AuthRequiredError as e:
			print('Your T1 credentials appear to be incorrect. '
					'Please check your configuration.')
			raise
		pass
		return result.attribs
	pass

pass
