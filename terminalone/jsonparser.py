# -*- coding: utf-8 -*-
"""Parses JSON output from T1 and returns a Python object"""

from __future__ import absolute_import

# Map known status.code repsonses to Exceptions. 'ok' signifies no exception,
# so that is None. 'invalid' can have many errors and needs
# an additional level of parsing, while the others can be instantiated directly.
STATUS_CODES = {
    'ok': None,
    'invalid': True,
    'not_found': NotFoundError,
    'auth_required': AuthRequiredError,
    'auth_error': AuthRequiredError,
    'error': APIError,
    'bad_request': ClientError,
}

class JSONParser(object):
	"""Parses JSON response"""

	def __init__(self, content):
		json = 
