# -*- coding: utf-8 -*-
"""Provides deal object for PMP-E and Global Deals."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Deal(Entity):
    """docstring for deals."""
    collection = 'deals'
    resource = 'deal'
    _bill_types = t1types.enum({'EXCHANGE', 'PUBLISHER', 'NONE'}, 'EXCHANGE')
    _price_methods = t1types.enum({'CPM'}, 'CPM')
    _price_types = t1types.enum({'FIXED', 'FLOOR'}, None)
    _pull = {
        'created_on': t1types.strpt,
        'deal_identifier': None,
        'description': None,
        'end_datetime': t1types.strpt,
        'id': int,
        'name': None,
        'bill_type': None,
        'owner': dict,
        'price': dict,
        'price_method': None,
        'price_type': None,
        'start_datetime': t1types.strpt,
        'status': bool,
        'supply_source_id': int,
        'sub_supply_source_id': int,
        'updated_on': t1types.strpt,
        'zone_name': None,
    }
    _push = _pull.copy()
    _push.update({
        'bill_type': _bill_types,
        'end_datetime': t1types.strft,
        'price_method': _price_methods,
        'price_type': _price_types,
        'start_datetime': t1types.strft,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(Deal, self).__init__(session, properties, **kwargs)

