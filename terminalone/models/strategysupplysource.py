# -*- coding: utf-8 -*-
"""Provides strategy supply source object."""

from __future__ import absolute_import
from ..entity import Entity


class StrategySupplySource(Entity):
    """StrategySupplySource object, for strategies targeting not-all-exchanges."""
    collection = 'strategy_supply_sources'
    resource = 'strategy_supply_source'
    _relations = {
        'strategy',
        'supply_source',
    }
    _pull = {
        'id': int,
        'strategy_id': int,
        'supply_source_id': int,
        'version': int,
    }
    _push = _pull

    def __init__(self, session, properties=None, **kwargs):
        super(StrategySupplySource, self).__init__(session, properties, **kwargs)
