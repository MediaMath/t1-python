# -*- coding: utf-8 -*-
"""Provides strategy day part object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class StrategyDayPart(Entity):
    """StrategyDayPart object, for strategies targeting day parts."""
    collection = 'strategy_day_parts'
    resource = 'strategy_day_part'
    _relations = {
        'strategy',
    }
    _pull = {
        'created_on': t1types.strpt,
        'days': None,
        'end_hour': int,
        'id': int,
        'start_hour': int,
        'status': t1types.int_to_bool,
        'strategy_id': int,
        'udpated_on': t1types.strpt,
        'user_time': t1types.int_to_bool,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'status': int,
        'user_time': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(StrategyDayPart, self).__init__(session, properties, **kwargs)

    def remove(self):
        """Unassign the strategy_day_part from the strategy."""
        url = '/'.join([self.collection,
                        str(self.id),
                        'delete'])
        self._post(self._get_service_path(), rest=url, data={'version': self.version})
        for item in list(self._properties.keys()):
            del self._properties[item]
