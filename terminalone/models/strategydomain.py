# -*- coding: utf-8 -*-
"""Provides strategy domain restriction object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class StrategyDomain(Entity):
    """Strategy domain restriction object."""
    collection = 'strategy_domain_restrictions'
    resource = 'strategy_domain_restriction'
    _relations = {
        'strategy',
    }
    _restrictions = t1types.enum({'INCLUDE', 'EXCLUDE'}, '')
    _pull = {
        'created_at': t1types.strpt,
        'domain': None,
        'id': int,
        'restriction': None,
        'strategy_id': int,
        'updated_on': t1types.strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'restriction': _restrictions,
    })
    _readonly = Entity._readonly | {'created_at', }

    def __init__(self, session, properties=None, **kwargs):
        super(StrategyDomain, self).__init__(session, properties, **kwargs)
