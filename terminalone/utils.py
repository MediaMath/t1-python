# -*- coding: utf-8 -*-
"""Constants for ease of importing.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

import csv
from functools import reduce

class filters(object):
	IN = '()'
	NULL = ':'
	NOT_NULL = ':!'
	# Equals operator is *different* between M&E (==) and Picard (=)
	EQUALS = '=='
	NOT_EQUALS = '!='
	GREATER = '>'
	GREATER_OR_EQUAL = '>='
	LESS = '<'
	LESS_OR_EQUAL = '<='
	CASE_INS_STRING = '=:'
	# Following are not available in M&E API
	# CASE_INS_NOT_STRING = '!:'
	# CASE_SENS_STRING = '=~'
	# CASE_SENS_NOT_STRING = '!~'

def compose(*functions):
	return reduce(lambda f, g: lambda x: f(g(x)), functions)

def dpath(d, path):
	from operator import getitem
	paths = path.split('.')
	return reduce(
		lambda x, y: getitem(x, y),
		paths,
		d
	)

def credentials(filename=None, root=None):
	"""Get credentials from JSON file or environment variables.
	
	JSON file should have credentials in the form of:
	{
		"username": "myusername",
		"password": "supersecret",
		"api_key": "myapikey"
	}

	If filename not provided, fall back on environment variables:
	- T1_API_USERNAME
	- T1_API_PASSWORD
	- T1_API_KEY

	:param filename: str filename of JSON file containing credentials.
	:param root: str path to get to credentials object. For instance, in object:
		{
			"credentials": {
				"api": {
					"username": "myusername",
					"password": "supersecret",
					"api_key": "myapikey"
				}
			}
		}
		"root" is "credentials.api"
	:return: dict[str]str
	:raise: TypeError: no JSON file or envvars
	"""

	if filename is not None:
		import json
		with open(filename, 'rb') as f:
			conf = json.load(f)
		if root is not None:
			conf = dpath(conf, root)
	else:
		import os
		try:
			conf = {
				'username': os.environ['T1_API_USERNAME'],
				'password': os.environ['T1_API_PASSWORD'],
				'api_key': os.environ['T1_API_KEY'],
			}
		except KeyError:
			raise TypeError('Must either supply JSON file of credentials'
				' or set environment variables T1_API_{USERNAME,PASSWORD,KEY}')

	return conf
