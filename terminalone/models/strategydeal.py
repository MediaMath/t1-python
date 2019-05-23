# -*- coding: utf-8 -*-
"""Provides strategy deal object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class StrategyDeal(Entity):
    """StrategyDeal object to join strategy and deals."""
    collection = 'strategy_deals'
    resource = 'strategy_deal'
    _relations = {
        'deal',
        'strategy',
    }

    _pull = {
        'deal_id': int,
        'id': int,
        'strategy_id': int,
        'version': int,
    }
    _push = _pull.copy()

    _readonly = Entity._readonly | {'deal_id', 'strategy_id', 'version'}

    def __init__(self, session, properties=None, **kwargs):
        super(StrategyDeal, self).__init__(session, properties, **kwargs)

    def remove(self):
        """Unassign the deal from the strategy."""
        url = '/'.join([self.collection,
                        str(self.id),
                        'delete'])
        self._post(self._get_service_path(), rest=url, data={'version': self.version})
        for item in list(self._properties.keys()):
            del self._properties[item]
