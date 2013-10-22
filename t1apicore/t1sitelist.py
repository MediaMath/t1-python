# -*- coding: utf-8 -*-
"""Provides site list object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import T1Object

class T1SiteList(T1Object):
	"""docstring for T1SiteList."""
	collection = 'site_lists'
	type = 'site_list'
	_restrictions = T1Object._enum({'INCLUDE', 'EXCLUDE'}, 'EXCLUDE')
	_pull = {
		'created_on': T1Object._strpt,
		'filename': str,
		'id': int,
		'name': str,
		'organization_id': int,
		'restriction': str,
		'status': T1Object._int_to_bool,
		'updated_on': T1Object._strpt,
		'version': int,
	}
	_push = _pull.copy()
	_push.update({
		'restriction': _restrictions,
		'status': int,
	})
	_readonly = T1Object._readonly.copy()
	def __init__(self, auth, properties=None):
		super(T1SiteList, self).__init__(auth, properties)
