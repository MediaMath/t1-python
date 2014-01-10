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
		'address_1': str,
		'address_2': str,
		'adx_seat_account_id': int,
		'allow_byo_price': T1Object._int_to_bool,
		'allow_x_agency_pixels': T1Object._int_to_bool,
		'city': str,
		'contact_name': str,
		'country': str,
		'created_on': T1Object._strpt,
		'curency_code': str,
		'id': int,
		'mm_contact_name': str,
		'name': str,
		'phone': str,
		'state': str,
		'status': T1Object._int_to_bool,
		'tag_ruleset': str,
		'updated_on': T1Object._strpt,
		'use_evidon_optout': T1Object._int_to_bool,
		'version': int,
		'zip': str,
	}
	_push = _pull.copy()
	_push.update({
		'allow_byo_price': int,
		'allow_x_agency_pixels': int,
		'status': int,
		'use_evidon_optout': int,
	})
	_readonly = T1Object._readonly.copy()
	def __init__(self, auth, properties=None):
		super(T1Organization, self).__init__(auth, properties)
