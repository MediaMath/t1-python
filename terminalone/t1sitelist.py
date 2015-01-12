# -*- coding: utf-8 -*-
"""Provides site list object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from .t1object import T1Object

class T1SiteList(T1Object):
	"""docstring for T1SiteList."""
	collection = 'site_lists'
	type = 'site_list'
	_relations = {
		'organization',
	}
	_restrictions = T1Object._enum({'INCLUDE', 'EXCLUDE'}, 'EXCLUDE')
	_pull = {
		'created_on': T1Object._strpt,
		'filename': None,
		'id': int,
		'name': None,
		'organization_id': int,
		'restriction': None,
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
	def __init__(self, session, properties=None, **kwargs):
		super(T1SiteList, self).__init__(session, properties, **kwargs)
