# -*- coding: utf-8 -*-
"""Provides agency object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from ..entity import Entity

class Agency(Entity):
	"""docstring for Agency"""
	collection = 'agencies'
	type = 'agency'
	_relations = {
		'organization', 'billing_contact', 'sales_contact',
		'traffic_contact',
	}
	_pull = {
		'allow_x_adv_optimization': Entity._int_to_bool,
		'allow_x_adv_pixels': Entity._int_to_bool,
		'billing_contact_id': int,
		'created_on': Entity._strpt,
		'id': int,
		'logo': None,
		'name': None,
		'organization_id': int,
		'sales_contact_id': int,
		'status': Entity._int_to_bool,
		'updated_on': Entity._strpt,
		'version': int,
	}
	_push = _pull.copy()
	_push.update({
		'allow_x_adv_optimization': int,
		'allow_x_adv_pixels': int,
		'status': int,
	})
	_readonly = Entity._readonly.copy()
	def __init__(self, session, properties=None, **kwargs):
		super(Agency, self).__init__(session, properties, **kwargs)
