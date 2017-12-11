# -*- coding: utf-8 -*-
"""Provides retired strategy audience segment object."""

from __future__ import absolute_import

from terminalone.errors import ClientError
from .. import t1types
from ..entity import Entity


class RetiredStrategyAudienceSegment(Entity):
    """Object for retired strategy targeting third-party segments."""
    collection = 'retired_strategy_audience_segments'
    resource = 'retired_strategy_audience_segment'
    _relations = {
        'audience_segment',
        'strategy',
    }
    _pull = {
        'strategy_id': int,
        'retired_audience_segment_id': int,
        'version': int,
        'name': None,
        'updated_on': t1types.strpt,
        'group_identifier': None,
        'created_on': t1types.strpt,
        'id': int,
        'restriction': None,
    }
    _push = _pull.copy()
    _readonly = Entity._readonly | {'name', }

    def __init__(self, session, properties=None, **kwargs):
        super(RetiredStrategyAudienceSegment, self).__init__(session, properties, **kwargs)

    def save(self, *args, **kwargs):
        raise ClientError('This object is not editable.')
