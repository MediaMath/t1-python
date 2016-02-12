# -*- coding: utf-8 -*-
"""Provides seat object."""

from __future__ import absolute_import
from ..entity import Entity


class Seat(Entity):
    """Seat entity."""
    collection = 'seats'
    resource = 'seat'
    _relations = {
        'advertiser',
    }
    _rmx_units = Entity._enum({'CPM', 'PCT_MEDIA'}, 'PCT_MEDIA')
    _pull = {
        'bill_media_to_client': Entity._int_to_bool,
        'created_on': Entity._strpt,
        'id': int,
        'organization_id': int,
        'rmx_exchange_cost_cpm': float,
        'rmx_exchange_cost_pct': float,
        'rmx_exchange_cost_unit': None,
        'seat_identifier': None,
        'status': Entity._int_to_bool,
        'supply_source_id': int,
        'updated_on': Entity._strpt,
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
