# -*- coding: utf-8 -*-
"""Provides exception and error handling for T1 API calls.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

KNOWN_CODES = {'ok': None, 'auth_required': 'Authentication Required',
				'invalid': set(['Validation Errors', 'Login Incorrect']),
				'not_found': 'Entity Not Found'}
# auth_required also has 'reason': 'not_logged_in'. Incorrect auths get 'invalid': 'Login Incorrect'

class T1BaseException(Exception):
	"""Base Exception for the module"""
	pass

class T1ClientError(T1BaseException):
	"""Used for improper usages of the module.
	
	Improper usage includes attempting to retrieve a collection not in T1,
	attempting to send data that doesn't match an API object, etc.
	"""
	pass

class T1APIError(T1BaseException):
	"""Base class that includes error code and message.
	
	Takes two arguments (minus self), the API error code and message. This allows
	for the Exception to include both args.
	"""
	def __init__(self, code, message):
		self.code = code
		self.message = message
	def __str__(self):
		return repr("{}: {}".format(self.code, self.message))

class T1Error(T1APIError):
	"""docstring for T1Error"""
	def __str__(self):
		return repr('Uknown error: {}: {}'.format(self.code, self.message))

class T1AuthRequiredError(T1APIError):
	"""docstring for T1AuthenticationRequired"""
	pass

class T1ValidationError(T1APIError):
	"""docstring for T1ValidationError"""
	def __init__(self, code, errors):
		msg_list = ['{} (code: {}): {}'.format(error, val['code'], val['error'])
			for (error, val) in errors.iteritems()]
		messages = [code] + msg_list
		self.message = '\n'.join(messages)
	def __str__(self):
		return self.message

class T1NotFoundError(T1APIError):
	"""docstring for T1NotFoundError"""
	pass

class T1LoginError(T1BaseException):
	"""Exception class for invalid T1 Logins. Returns details of invalid login.
	
	If you encounter this class, it's because there's an issue with your T1 login.
	Logins are defined in the config file, and need to be kept up-to-date.
	"""
	def __init__(self, code, message, credentials):
		self.code = code
		self.message = message
		self.credentials = credentials
	def __str__(self):
		return repr('{}: {} -- {}'.format(self.code, self.message,
											self.credentials))
