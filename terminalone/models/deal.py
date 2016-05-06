# -*- coding: utf-8 -*-
"""Provides deal object for PMP-E and Global Deals."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Deal(Entity):
    """docstring for deals."""
    collection = 'deals'
    resource = 'deal'
    _relations = {
        'advertiser',
        'publisher',
        'supply_source',
    }
    _deal_sources = t1types.enum({'USER', 'INTERNAL'}, 'INTERNAL')
    _media_types = t1types.enum({'DISPLAY', 'VIDEO'}, 'DISPLAY')
    _price_methods = t1types.enum({'CPM'}, 'CPM')
    _price_types = t1types.enum({'FIXED', 'FLOOR'}, None)
    _pull = {
        'advertiser_id': int,
        'created_on': t1types.strpt,
        'currency_code': None,
        'deal_identifier': None,
        'deal_source': None,
        'description': None,
        'end_datetime': t1types.strpt,
        'id': int,
        'media_type': None,
        'name': None,
        'partner_sourced': t1types.int_to_bool,
        'price': float,
        'price_method': None,
        'price_type': None,
        'publisher_id': int,
        'start_datetime': t1types.strpt,
        'status': t1types.int_to_bool,
        'supply_source_id': int,
        'updated_on': t1types.strpt,
        'version': int,
        'zone_name': None,
    }
    _push = _pull.copy()
    _push.update({
        'deal_source': _deal_sources,
        'end_datetime': t1types.strft,
        'media_type': _media_types,
        'partner_sourced': int,
        'price_method': _price_methods,
        'price_type': _price_types,
        'start_datetime': t1types.strft,
        'status': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(Deal, self).__init__(session, properties, **kwargs)
