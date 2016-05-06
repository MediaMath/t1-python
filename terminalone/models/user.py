# -*- coding: utf-8 -*-
"""Provides user object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class User(Entity):
    """User entity."""
    collection = 'users'
    resource = 'user'
    _relations = {
        'creator',
    }
    _role = t1types.enum({'ADMIN', 'MANAGER', 'REPORTER'}, 'REPORTER')
    _scope = t1types.enum({'GLOBAL', 'SELECT'}, 'SELECT')
    _type = t1types.enum({'INTERNAL', 'AGENCY', 'VPAN', 'ADVERTISER'},
                         'ADVERTISER')
    _pull = {
        'access_internal_fees': t1types.int_to_bool,
        'active': t1types.int_to_bool,
        'created_on': t1types.strpt,
        'creator_id': int,
        'edit_data_definition': t1types.int_to_bool,
        'edit_campaigns': t1types.int_to_bool,
        'edit_margins_and_performance': t1types.int_to_bool,
        'edit_segments': t1types.int_to_bool,
        'fax': None,
        'first_name': None,
        'id': int,
        'labs_enable_rmx': t1types.int_to_bool,
        'last_login_on': t1types.strpt,
        'last_name': None,
        'link_ldap': t1types.int_to_bool,
        'mobile': None,
        'password': None,
        'password_reset_sent': t1types.strpt,
        'password_reset_token': None,
        'phone': None,
        'role': None,
        'scope': None,
        'sso_auth_sent': t1types.strpt,
        'sso_auth_token': None,
        'title': None,
        'type': None,
        'updated_on': t1types.strpt,
        'username': None,
        'version': int,
        'view_data_definition': t1types.int_to_bool,
        'view_dmp_reports': t1types.int_to_bool,
        'view_organizations': t1types.int_to_bool,
        'view_segments': t1types.int_to_bool,
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
