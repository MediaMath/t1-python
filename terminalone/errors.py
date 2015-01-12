# -*- coding: utf-8 -*-
"""Provides exception and error handling for T1 API calls.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import

class T1Error(Exception):
	"""Base exception class for the module. To catch all errors, catch this.

	T1Error encompasses errors that occur both from the client
	(bad request, bad formation of properties, etc), to errors returned by the
	server (validation errors, login errors, etc). Sets code and message attributes.
	"""
	def __init__(self, code, message):
		self.code = code
		self.message = message
	def __str__(self):
		return repr('Error: {}: {}'.format(self.code, self.message))

class ClientError(T1Error):
	"""Used for improper usages of the module.

	Improper usage includes attempting to retrieve a collection not in T1,
	attempting to send data that doesn't match an API object, etc.
	"""
	pass
T1ClientError = ClientError

class APIError(T1Error):
	"""Base class that includes error code and message."""
	pass
T1APIError = APIError

# class T1Error(T1APIError):
# 	"""docstring for T1Error"""
# 	def __str__(self):
# 		return repr('Unknown error: {}: {}'.format(self.code, self.message))

class AuthRequiredError(APIError):
	"""docstring for AuthenticationRequired"""
	pass

class ValidationError(APIError):
	"""docstring for ValidationError"""
	def __init__(self, code, errors):
		msg_list = ['{} (code: {}): {}'.format(error, val['code'], val['error'])
			for (error, val) in errors.iteritems()]
		messages = [code] + msg_list
		self.message = '\n'.join(messages)
	def __str__(self):
		return self.message

class NotFoundError(APIError):
	"""docstring for NotFoundError"""
	pass

class LoginError(T1Error):
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
