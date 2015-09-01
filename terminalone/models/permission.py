# -*- coding: utf-8 -*-
"""Provides permission object."""

from __future__ import absolute_import
from ..errors import ClientError
from ..entity import SubEntity


class Permission(SubEntity):
    """docstring for Permission."""
    collection = 'permissions'
    resource = 'permission'

    _pull = {
        '_type': None,
        'advertiser': None,
        'agency': None,
        'organization': None,
        'edit_data_definition': int,
        'view_data_definition': int,
        'edit_segments': int,
        'edit_campaigns': int,
        'access_internal_fees': int,
        'edit_margins_and_performance': int,
        'view_organizations': int,
        'view_segments': int,
        'view_dmp_reports': int,
        'type': None,
        'role': None,
        'scope': None,
    }

    def __init__(self, session, properties=None, **kwargs):
        super(Permission, self).__init__(session, properties, **kwargs)

    def save(self, *args, **kwargs):
        raise ClientError('Temporarily not editable - update coming soon!')
