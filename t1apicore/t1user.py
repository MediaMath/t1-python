# -*- coding: utf-8 -*-
"""Provides user object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

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
		'fax': str,
		'first_name': str,
		'id': int,
		'labs_enable_rmx': T1Object._int_to_bool,
		'last_login_on': T1Object._strpt,
		'last_name': str,
		'link_ldap': T1Object._int_to_bool,
		'mobile': str,
		'password': str,
		'password_reset_sent': T1Object._strpt,
		'password_reset_token': str,
		'phone': str,
		'role': str,
		'scope': str,
		'sso_auth_sent': T1Object._strpt,
		'sso_auth_token': str,
		'title': str,
		'type': str,
		'updated_on': T1Object._strpt,
		'username': str,
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
	def __init__(self, auth, properties=None):
		super(T1User, self).__init__(auth, properties)
