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

# class T1BaseException(Exception):
# 	"""Base Exception for T1LoginError."""
# 	pass

# class T1LoginError(T1BaseException):
# 	"""docstring for T1LoginError"""
# 	def __init__(self, code, message, credentials):
# 		# super(T1LoginError, self).__init__()
# 		self.code = code
# 		self.message = message
# 		self.credentials = credentials
# 	def __str__(self):
# 		return repr(self.code.capitalize() + ": " + self.message + ' -- ' + credentials)

class Error(Exception):
	pass

class T1Error(object):
	"""docstring for T1Error"""
	def __init__(self, code, message):
		# super(T1Error, self).__init__()
		self.code = code
		self.message = message
		pass
	pass

class T1ValidationError(object):
	"""docstring for T1ValidationError"""
	def __init__(self, code, message):
		# super(T1ValidationError, self).__init__()
		self.code = code
		self.message = message
		pass
	pass

class T1NotFoundError(object):
	"""docstring for T1NotFoundError"""
	def __init__(self, code, message):
		# super(T1NotFoundError, self).__init__()
		self.code = code
		self.message = message
		pass
	pass

class T1Exception(Exception):
	"""docstring for T1Exception"""
	def __init__(self, arg):
		# super(T1Exception, self).__init__()
		self.arg = arg
		pass
	pass
