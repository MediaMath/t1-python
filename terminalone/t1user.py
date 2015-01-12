# -*- coding: utf-8 -*-
"""Provides user object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from .t1object import T1Object

class T1User(T1Object):
	"""docstring for T1User."""
	collection = 'users'
	type = 'user'
	_relations = {
		'creator',
	}
	_role = T1Object._enum({'ADMIN', 'MANAGER', 'REPORTER'}, 'REPORTER')
	_scope = T1Object._enum({'GLOBAL', 'SELECT'}, 'SELECT')
	_type = T1Object._enum({'INTERNAL', 'AGENCY', 'VPAN', 'ADVERTISER'},
							'ADVERTISER')
	_pull = {
		'access_internal_fees': T1Object._int_to_bool,
		'active': T1Object._int_to_bool,
		'created_on': T1Object._strpt,
		'creator_id': int,
		'edit_campaigns': T1Object._int_to_bool,
		'edit_margins_and_performance': T1Object._int_to_bool,
		'fax': None,
		'first_name': None,
		'id': int,
		'labs_enable_rmx': T1Object._int_to_bool,
		'last_login_on': T1Object._strpt,
		'last_name': None,
		'link_ldap': T1Object._int_to_bool,
		'mobile': None,
		'password': None,
		'password_reset_sent': T1Object._strpt,
		'password_reset_token': None,
		'phone': None,
		'role': None,
		'scope': None,
		'sso_auth_sent': T1Object._strpt,
		'sso_auth_token': None,
		'title': None,
		'type': None,
		'updated_on': T1Object._strpt,
		'username': None,
		'version': int,
		'view_organizations': T1Object._int_to_bool,
	}
	_push = _pull.copy()
	_push.update({
		'access_internal_fees': int,
		'active': int,
		'edit_campaigns': int,
		'edit_margins_and_performance': int,
		'labs_enable_rmx': int,
		'link_ldap': int,
		'role': _role,
		'scope': _scope,
		'type': _type,
		'view_organizations': int,
	})
	_readonly = T1Object._readonly.copy()
	def __init__(self, session, properties=None, **kwargs):
		super(T1User, self).__init__(session, properties, **kwargs)
