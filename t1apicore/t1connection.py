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
	def __init__(self, environment='sandbox'):
		self.config = self.load_config('t1api.{}.json'.format(environment if environment 
															in T1Connection.VALID_ENVS else 'sandbox'))
		# super(T1Connection, self).__init__()
		self.t1nowtime = lambda: int(time())
		self.adama_session = requests.Session()
		self.cookie_file = self.config['cookie_path']
		if isfile(self.cookie_file) and getsize(self.cookie_file) > 0:
			with open(self.cookie_file) as f:
				self.adama_session.cookies = cookiejar_from_dict(pickle.load(f))
		self.api_base = 'https://' + self.config['base_uri']
		if not hasattr(self, 'active'):
			self.check_session()
		elif not self.active:
			self.check_session()
	
	def check_session(self):
		response = self.adama_session.get(self.api_base + '/session', stream=True,
											params={'nowTime': self.t1nowtime()})
		session_check = T1RawParse(response.raw)
		status_code = session_check.find('status').get('code')
		if status_code == 'ok':
			self.active = True
		elif status_code == 'auth_required':
			# if isfile(self.cookie_file) and getsize(self.cookie_file) > 0:
			# 	with open(self.cookie_file) as f:
			# 		self.adama_session.cookies = cookiejar_from_dict(pickle.load(f))
			self.open_connection()
			self.active = True
			with open(self.cookie_file, 'w') as f:
				pickle.dump(dict_from_cookiejar(self.adama_session.cookies), f)
	
	def open_connection(self):
		"""This is used to log in"""
		credentials = {'user': self.config['username'],
						'password': self.config['password']}
		login_response = self.adama_session.post(self.api_base + '/login',
												params=credentials, stream=True)
		result = T1RawParse(login_response.raw)
		status_code = result.find('status').get('code')
		if status_code == 'ok':
			return None
		elif status_code == 'invalid' or status_code == 'auth_error':
			raise T1LoginError(status_code, result.find('status').text, credentials)
		pass
	
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
		if not self.active:
			self.open_connection()
		while True:
			try:
				response = self.adama_session.get(url, params=params, stream=True)
				result = T1XMLParser(response.raw)
				break
			except T1AuthRequiredError:
				self.check_session()
			# except T1Error: # If xmlparser is going to raise it anyway, why re-raise it here?
			# 	raise
		pass
		return result.attribs
	
	def _post(self, url, data):
		"""Base method for subclasses to call."""
		if not data:
			raise requests.exceptions.RequestException('No POST data.')
		if not self.active:
			self.open_connection()
		while True:
			try:
				response = self.adama_session.post(url, data=data, stream=True)
				result = T1XMLParser(response.raw)
				break
			except T1AuthRequiredError:
				self.check_session()
			# except T1Error:
			# 	raise
		pass
		return result.attribs
	pass

pass
