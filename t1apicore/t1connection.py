# -*- coding: utf-8 -*-
"""Provides connection object for T1.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it. Uses json and cPickle/pickle to serialize cookie objects.
"""

from time import time
# import contextlib
import json
try:
	import cPickle as pickle
except ImportError:
	import pickle
import requests
from requests.utils import dict_from_cookiejar#, cookiejar_from_dict
import xmlparser

# API_BASE = 'https://t1.mediamath.com/api/v1/'
T1NOWTIME = lambda: int(time())
T1_API_ENV = 'production'

class T1LoginException(Exception):
	"""Base Exception for T1LoginError."""
	pass
class T1LoginError(T1LoginException):
	"""Exception class for invalid T1 Logins. Returns details of invalid login.
	
	If you encounter this class, it's because there's an issue with your T1 login.
	Logins are define in the config file, and need to be kept up-to-date.
	"""
	def __init__(self, code, message, credentials):
		# super(T1LoginError, self).__init__()
		self.code = code
		self.message = message
		self.credentials = credentials
	def __str__(self):
		return repr(self.code.capitalize() + ": " + self.message + ' -- ' + self.credentials)

class T1Connection(object):
	"""docstring for T1Connection"""
	VALID_ENVS = frozenset(['production', 'sandbox'])
	def __init__(self, environment='sandbox'):
		self.config = self.load_config('t1api.{}.json'.format(environment if environment 
															in T1Connection.VALID_ENVS else 'sandbox'))
		# super(T1Connection, self).__init__()
		self.cookie_file = self.config['cookie_path']
		self.adama_session = requests.Session()
		with open(self.cookie_file) as f:
			self.adama_session.cookies = pickle.load(f)
		self.api_base = 'https://' + self.config['base_uri']
		# Test connection by getting the session data and checking the status code
		session_response = self.adama_session.get(self.api_base + '/session', stream=True,
												params={'nowTime': T1NOWTIME()})
		session_check = xmlparser.T1RawParse(session_response.raw)
		status_code = session_check.find('status').get('code')
		if status_code == 'ok':
			self.active = True
		elif status_code == 'auth_required':
			self.open_connection()
			self.active = True
		with open(self.cookie_file, 'w') as f:
			pickle.dump(dict_from_cookiejar(self.adama_session.cookies), f)
		pass
	
	def open_connection(self):
		"""This is used to log in"""
		credentials = {'user': self.config['username'],
						'password': self.config['password']}
		login_response = self.adama_session.post(self.api_base + '/login',
												params=credentials, stream=True)
		result = xmlparser.T1RawParse(login_response.raw)
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
		response = self.adama_session.get(url, params=params, stream=True)
		result = xmlparser.T1XMLParser(response)
		pass
		return result.attribs
	
	def _post(self, url, data):
		"""Base method for subclasses to call."""
		if not data:
			raise requests.exceptions.RequestException('No POST data.')
		if not self.active:
			self.open_connection()
		response = self.adama_session.post(url, data=data, stream=True)
		result = xmlparser.T1XMLParser(response)
		pass
		return result.attribs
	pass

pass
