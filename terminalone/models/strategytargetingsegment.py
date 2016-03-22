# -*- coding: utf-8 -*-
"""Provides strategy targeting segment object."""

from __future__ import absolute_import
from ..config import PATHS
from ..entity import Entity


class StrategyTargetingSegment(Entity):
    """docstring for StrategyTargetingSegment."""
    collection = 'strategy_targeting_segments'
    resource = 'strategy_targeting_segment'
    _relations = {
        'targeting_segment',
        'strategy',
    }
    _pull = {
        'created_on': Entity._strpt,
        'group_identifier': None,
        'id': int,
        'operator': None,
        'restriction': None,
        'strategy_id': int,
        'targeting_segment_id': int,
        'type': None,
        'updated_on': Entity._strpt,
        'user_cpm': float,
        'version': int,
    }
    _push = _pull.copy()
    _readonly = Entity._readonly | {'name', }

    def __init__(self, session, properties=None, **kwargs):
        super(StrategyTargetingSegment, self).__init__(session, properties, **kwargs)

    def remove(self):
        """Unassign the strategy targeting segment from the strategy."""
        url = '/'.join(['strategies',
                        str(self.parent_id),
                        'targeting_segments'])
        data = {
            'segments.1.id': str(-1 * self.targeting_segment_id),
            'segments.1.restriction': self.restriction,
            'segments.1.group_identifier': self.group_identifier,
            'exclude_op': 'OR',
            'include_op': 'OR',
        }
        self._post(PATHS['mgmt'], rest=url, data=data)
        for item in list(self.properties.keys()):
            del self.properties[item]
