# -*- coding: utf-8 -*-
"""Provides user object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from ..entity import Entity

class User(Entity):
	"""docstring for User."""
	collection = 'users'
	resource = 'user'
	_relations = {
		'creator',
	}
	_role = Entity._enum({'ADMIN', 'MANAGER', 'REPORTER'}, 'REPORTER')
	_scope = Entity._enum({'GLOBAL', 'SELECT'}, 'SELECT')
	_type = Entity._enum({'INTERNAL', 'AGENCY', 'VPAN', 'ADVERTISER'},
							'ADVERTISER')
	_pull = {
		'access_internal_fees': Entity._int_to_bool,
		'active': Entity._int_to_bool,
		'created_on': Entity._strpt,
		'creator_id': int,
		'edit_campaigns': Entity._int_to_bool,
		'edit_margins_and_performance': Entity._int_to_bool,
		'fax': None,
		'first_name': None,
		'id': int,
		'labs_enable_rmx': Entity._int_to_bool,
		'last_login_on': Entity._strpt,
		'last_name': None,
		'link_ldap': Entity._int_to_bool,
		'mobile': None,
		'password': None,
		'password_reset_sent': Entity._strpt,
		'password_reset_token': None,
		'phone': None,
		'role': None,
		'scope': None,
		'sso_auth_sent': Entity._strpt,
		'sso_auth_token': None,
		'title': None,
		'type': None,
		'updated_on': Entity._strpt,
		'username': None,
		'version': int,
		'view_organizations': Entity._int_to_bool,
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
	_readonly = Entity._readonly.copy()
	def __init__(self, session, properties=None, **kwargs):
		super(User, self).__init__(session, properties, **kwargs)
