# -*- coding: utf-8 -*-
"""Provides agency object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import T1Object

class T1Organization(T1Object):
	"""docstring for T1Organization"""
	collection = 'organizations'
	type = 'organization'
	_relations = {
		'currency',
	}
	_pull = {
		'address_1': None,
		'address_2': None,
		'adx_seat_account_id': int,
		'allow_byo_price': T1Object._int_to_bool,
		'allow_x_agency_pixels': T1Object._int_to_bool,
		'city': None,
		'contact_name': None,
		'country': None,
		'created_on': T1Object._strpt,
		'curency_code': None,
		'id': int,
		'mm_contact_name': None,
		'name': None,
		'phone': None,
		'state': None,
		'status': T1Object._int_to_bool,
		'tag_ruleset': None,
		'updated_on': T1Object._strpt,
		'use_evidon_optout': T1Object._int_to_bool,
		'version': int,
		'zip': None,
	}
	_push = _pull.copy()
	_push.update({
		'allow_byo_price': int,
		'allow_x_agency_pixels': int,
		'status': int,
		'use_evidon_optout': int,
	})
	_readonly = T1Object._readonly.copy()
	def __init__(self, session, properties=None, **kwargs):
		super(T1Organization, self).__init__(session, properties, **kwargs)
