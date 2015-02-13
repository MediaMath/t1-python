# -*- coding: utf-8 -*-
"""Constants for ease of importing.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

class filters(object):
	IN = '()'
	NULL = ':'
	NOT_NULL = ':!'
	# Equals operator is *different* between M&E (==) and Picard (=)
	EQUALS = '=='
	NOT_EQUAL = '!='
	GREATER = '>'
	GREATER_OR_EQUAL = '>='
	LESS = '<'
	LESS_OR_EQUAL = '<='
	CASE_INS_STRING = '=:'
	# Following are not available in M&E API
	# CASE_INS_NOT_STRING = '!:'
	# CASE_SENS_STRING = '=~'
	# CASE_SENS_NOT_STRING = '!~'
