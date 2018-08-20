# -*- coding: utf-8 -*-
"""Provides budget_flight object."""

from __future__ import absolute_import

from .. import t1types
from ..entity import SubEntity


class BudgetFlight(SubEntity):
    """Budget Flight entity."""
    collection = 'budget_flights'
    resource = 'budget_flight'
    _relations = {
        'campaign',
    }

    _pull = {
        'campaign_id': int,
        'created_on': t1types.strpt,
        'currency_code': None,
        'end_date': t1types.strpt,
        'id': int,
        'is_relevant': bool,
        'name': None,
        'start_date': t1types.strpt,
        'total_budget': float,
        'updated_on': t1types.strpt,
        'version': int,
        'zone_name': None,
    }
    _push = _pull.copy()
    _push.update({
        'is_relevant': int,
        'end_date': t1types.strft,
        'start_date': t1types.strft,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(BudgetFlight, self).__init__(session, properties, **kwargs)
