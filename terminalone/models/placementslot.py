# -*- coding: utf-8 -*-
"""Provides placement_slot object."""

from __future__ import absolute_import
from datetime import datetime
from .. import t1types
from ..entity import Entity
from ..vendor import six


def update_low_priority(original, candidate):
    for item, value in six.iteritems(candidate):
        if item in original:
            continue
        original[item] = value


class PlacementSlot(Entity):
    """Site Placement for PMP-D."""
    collection = 'placement_slots'
    resource = 'placement_slot'
    _relations = {
        'placement',
    }
    defaults = {
        'ad_slot': 1,
        'auction_type': 'FIRST_PRICED',
        'budget': 1.0,
        'buy_price_type': 'CPM',
        'end_date': datetime(2012, 12, 31, 0, 0, 0),
        'est_volume': 0,
        'frequency_amount': 1,
        'frequency_interval': 'not-applicable',
        'frequency_type': 'no-limit',
        'sell_price': 0.0,
        'sell_price_type': 'CPM',
        'start_date': datetime(2012, 10, 1, 0, 0, 0),
        'volume_unit': 'impressions',
    }
    _auction_types = t1types.enum({'FIRST_PRICED', 'SECOND_PRICED'},
                                  'FIRST_PRICED')
    _price_types = t1types.enum({'CPM', }, 'CPM')
    _frequency_intervals = t1types.enum({'hour', 'day', 'week', 'month',
                                         'campaign', 'not-applicable'},
                                        'not-applicable')
    _frequency_types = t1types.enum({'even', 'asap', 'no-limit'}, 'no-limit')
    _volume_units = t1types.enum({'impressions', }, 'impressions')
    _pull = {
        'ad_slot': int,
        'allow_remnant': t1types.int_to_bool,
        'auction_type': None,
        'budget': float,
        'buy_price': float,
        'buy_price_type': None,
        'created_on': t1types.strpt,
        'description': None,
        'end_date': t1types.strpt,
        'est_volume': float,
        'frequency_amount': int,
        'frequency_interval': None,
        'frequency_type': None,
        'height': int,
        'id': int,
        'prm_pub_ceiling': float,
        'prm_pub_markup': float,
        'sell_price': float,
        'sell_price_type': None,
        'site_placement_id': int,
        'start_date': t1types.strpt,
        'updated_on': t1types.strpt,
        'version': int,
        'volume_unit': None,
        'width': int,
    }
    _push = _pull.copy()
    _push.update({
        'allow_remnant': int,
        'auction_type': _auction_types,
        'buy_price_type': _price_types,
        'frequency_interval': _frequency_intervals,
        'frequency_type': _frequency_types,
        'sell_price_type': _price_types,
        'volume_unit': _volume_units,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(PlacementSlot, self).__init__(session, properties, **kwargs)

    def save(self, data=None, url=None):
        """Set defaults for object before saving"""
        update_low_priority(self._properties, self.defaults)
        super(PlacementSlot, self).save()
