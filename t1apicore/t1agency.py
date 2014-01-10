# -*- coding: utf-8 -*-
"""Provides agency object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import T1Object

class T1Agency(T1Object):
	"""docstring for T1Agency"""
	collection = 'agencies'
	type = 'agency'
	_relations = {
		'organization', 'billing_contact', 'sales_contact',
		'traffic_contact',
	}
	_pull = {
		'allow_x_adv_optimization': T1Object._int_to_bool,
		'allow_x_adv_pixels': T1Object._int_to_bool,
		'billing_contact_id': int,
		'created_on': T1Object._strpt,
		'id': int,
		'logo': unicode,
		'name': unicode,
		'organization_id': int,
		'sales_contact_id': int,
		'status': T1Object._int_to_bool,
		'updated_on': T1Object._strpt,
		'version': int,
	}
	_push = _pull.copy()
	_push.update({
		'allow_x_adv_optimization': int,
		'allow_x_adv_pixels': int,
		'status': int,
	})
	_readonly = T1Object._readonly.copy()
	def __init__(self, auth, properties=None):
		super(T1Agency, self).__init__(auth, properties)
