# -*- coding: utf-8 -*-
"""Provides strategy audience segment object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class StrategyAudienceSegment(Entity):
    """Object for strategy targeting third-party segments."""
    collection = 'strategy_audience_segments'
    resource = 'strategy_audience_segment'
    _relations = {
        'audience_segment',
        'strategy',
    }
    _pull = {
        'audience_segment_id': int,
        'created_on': t1types.strpt,
        'group_identifier': None,
        'id': int,
        'operator': None,
        'restriction': None,
        'strategy_id': int,
        'type': None,
        'updated_on': t1types.strpt,
        'user_cpm': float,
        'version': int,
    }
    _push = _pull.copy()
    _readonly = Entity._readonly | {'name', }

    def __init__(self, session, properties=None, **kwargs):
        super(StrategyAudienceSegment, self).__init__(session, properties, **kwargs)

    def remove(self):
        """Unassign the strategy audience segment from the strategy."""
        url = '/'.join(['strategies',
                        str(self.parent_id),
                        'audience_segments'])
        data = {
            'segments.1.id': str(-1 * self.audience_segment_id),
            'segments.1.restriction': self.restriction,
            'segments.1.group_identifier': self.group_identifier,
            'exclude_op': 'OR',
            'include_op': 'OR',
        }
        self._post(self._get_service_path(), rest=url, data=data)
        for item in list(self._properties.keys()):
            del self._properties[item]
