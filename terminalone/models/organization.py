# -*- coding: utf-8 -*-
"""Provides agency object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from ..entity import Entity

class Organization(Entity):
	"""docstring for Organization"""
	collection = 'organizations'
	resource = 'organization'
	_relations = {
		'currency',
	}
	_pull = {
		'address_1': None,
		'address_2': None,
		'adx_seat_account_id': int,
		'allow_byo_price': Entity._int_to_bool,
		'allow_x_agency_pixels': Entity._int_to_bool,
		'city': None,
		'contact_name': None,
		'country': None,
		'created_on': Entity._strpt,
		'curency_code': None,
		'id': int,
		'mm_contact_name': None,
		'name': None,
		'phone': None,
		'state': None,
		'status': Entity._int_to_bool,
		'tag_ruleset': None,
		'updated_on': Entity._strpt,
		'use_evidon_optout': Entity._int_to_bool,
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
	def __init__(self, session, properties=None, **kwargs):
		super(Organization, self).__init__(session, properties, **kwargs)
