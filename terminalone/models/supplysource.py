# -*- coding: utf-8 -*-
"""Provides supply source object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class SupplySource(Entity):
    """SupplySource object"""
    collection = 'supply_sources'
    resource = 'supply_source'
    _relations = {
        'parent_supply',
    }
    _rtb_types = t1types.enum({'STANDARD', 'MARKETPLACE', 'BATCH'}, None)
    _supply_types = t1types.enum({'exchange', 'data'}, None)
    _pull = {
        'bidder_exchange_identifier': int,
        'code': None,
        'created_on': t1types.strpt,
        'default_seat_identifier': None,
        'distribute': t1types.int_to_bool,
        'has_display': t1types.int_to_bool,
        'has_mobile_display': t1types.int_to_bool,
        'has_mobile_video': t1types.int_to_bool,
        'has_video': t1types.int_to_bool,
        'id': int,
        'is_proservice': t1types.int_to_bool,
        'mm_safe': t1types.int_to_bool,
        'parent_supply_id': int,
        'pixel_tag': None,
        'pmp_enabled': t1types.int_to_bool,
        'rtb_enabled': t1types.int_to_bool,
        'rtb_type': None,
        'seat_enabled': t1types.int_to_bool,
        'status': t1types.int_to_bool,
        'supply_type': None,
        'updated_on': t1types.strpt,
        'use_pool': t1types.int_to_bool,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'distribute': int,
        'has_display': int,
        'has_mobile_display': int,
        'has_mobile_video': int,
        'has_video': int,
        'is_proservice': int,
        'mm_safe': int,
        'pmp_enabled': int,
        'rtb_enabled': int,
        'seat_enabled': int,
        'status': int,
        'use_pool': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(SupplySource, self).__init__(session, properties, **kwargs)
