# -*- coding: utf-8 -*-
"""Provides seat object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Seat(Entity):
    """Seat entity."""
    collection = 'seats'
    resource = 'seat'
    _relations = {
        'advertiser',
    }
    _rmx_units = t1types.enum({'CPM', 'PCT_MEDIA'}, 'PCT_MEDIA')
    _pull = {
        'bill_media_to_client': t1types.int_to_bool,
        'created_on': t1types.strpt,
        'id': int,
        'organization_id': int,
        'rmx_exchange_cost_cpm': float,
        'rmx_exchange_cost_pct': float,
        'rmx_exchange_cost_unit': None,
        'seat_identifier': None,
        'status': t1types.int_to_bool,
        'supply_source_id': int,
        'updated_on': t1types.strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'bill_media_to_client': int,
        'rmx_exchange_cost_unit': _rmx_units,
        'status': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(Seat, self).__init__(session, properties, **kwargs)
