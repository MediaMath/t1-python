# -*- coding: utf-8 -*-
"""Provides agency object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Agency(Entity):
    """Agency entity."""
    collection = 'agencies'
    resource = 'agency'
    _relations = {
        'organization', 'billing_contact', 'sales_contact',
        'traffic_contact',
    }
    _dmp_settings = t1types.enum({'disabled', 'inherits'}, 'inherits')
    _pull = {
        'allow_x_adv_optimization': t1types.int_to_bool,
        'allow_x_adv_pixels': t1types.int_to_bool,
        'billing_contact_id': int,
        'created_on': t1types.strpt,
        'dmp_enabled': None,
        'id': int,
        'logo': None,
        'name': None,
        'organization_id': int,
        'sales_contact_id': int,
        'status': t1types.int_to_bool,
        'traffic_contact_id': int,
        'updated_on': t1types.strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'allow_x_adv_optimization': int,
        'allow_x_adv_pixels': int,
        'dmp_enabled': _dmp_settings,
        'status': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(Agency, self).__init__(session, properties, **kwargs)
