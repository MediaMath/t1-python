# -*- coding: utf-8 -*-
"""Provides strategy day part object."""

from __future__ import absolute_import
from ..entity import Entity


class StrategyDayPart(Entity):
    """StrategyDayPart object, for strategies targeting day parts."""
    collection = 'strategy_day_parts'
    resource = 'strategy_day_part'
    _relations = {
        'strategy',
    }
    _pull = {
        'created_on': Entity._strpt,
        'days': None,
        'end_hour': int,
        'id': int,
        'start_hour': int,
        'status': Entity._int_to_bool,
        'strategy_id': int,
        'udpated_on': Entity._strpt,
        'user_time': Entity._int_to_bool,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'status': int,
        'user_time': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(StrategyDayPart, self).__init__(session, properties, **kwargs)
