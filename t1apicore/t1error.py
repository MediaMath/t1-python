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
	"""docstring for T1Exception"""
	pass

class T1Error(T1BaseException):
	"""docstring for T1Error"""
	def __init__(self, code, message):
		# super(T1Error, self).__init__()
		self.code = code
		self.message = message
		pass
	pass

class T1AuthenticationRequiredError(T1BaseException):
	"""docstring for T1AuthenticationRequired"""
	pass

class T1ValidationError(T1BaseException):
	"""docstring for T1ValidationError"""
	def __init__(self, code, message):
		# super(T1ValidationError, self).__init__()
		self.code = code
		self.message = message
		pass
	pass

class T1NotFoundError(T1BaseException):
	"""docstring for T1NotFoundError"""
	def __init__(self, code, message):
		# super(T1NotFoundError, self).__init__()
		self.code = code
		self.message = message
		pass
	pass

class T1LoginError(T1BaseException):
	"""Exception class for invalid T1 Logins. Returns details of invalid login.
	
	If you encounter this class, it's because there's an issue with your T1 login.
	Logins are defined in the config file, and need to be kept up-to-date.
	"""
	def __init__(self, code, message, credentials):
		# super(T1LoginError, self).__init__()
		self.code = code
		self.message = message
		self.credentials = credentials
	def __str__(self):
		return repr(self.code.capitalize() + ": " + self.message + ' -- ' + self.credentials)
