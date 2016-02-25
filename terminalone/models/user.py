# -*- coding: utf-8 -*-
"""Provides user object."""

from __future__ import absolute_import
from ..entity import Entity


class User(Entity):
    """User entity."""
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
        'edit_data_definition': Entity._int_to_bool,
        'edit_campaigns': Entity._int_to_bool,
        'edit_margins_and_performance': Entity._int_to_bool,
        'edit_segments': Entity._int_to_bool,
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
        'view_data_definition': Entity._int_to_bool,
        'view_dmp_reports': Entity._int_to_bool,
        'view_organizations': Entity._int_to_bool,
        'view_segments': Entity._int_to_bool,
    }
    _push = _pull.copy()
    _push.update({
        'access_internal_fees': int,
        'active': int,
        'edit_campaigns': int,
        'edit_data_definition': int,
        'edit_margins_and_performance': int,
        'edit_segments': int,
        'labs_enable_rmx': int,
        'link_ldap': int,
        'role': _role,
        'scope': _scope,
        'type': _type,
        'view_data_definition': int,
        'view_dmp_reports': int,
        'view_organizations': int,
        'view_segments': int,
    })
    _readonly = Entity._readonly | {
        'last_login_on',
        'password_reset_sent',
        'password_reset_token',
        'sso_auth_sent',
        'sso_auth_token'
    }

    def __init__(self, session, properties=None, **kwargs):
        super(User, self).__init__(session, properties, **kwargs)
