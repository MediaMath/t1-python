# -*- coding: utf-8 -*-
"""Provides budget_flight object."""

from __future__ import absolute_import

from .. import t1types
from ..entity import Entity


class BudgetFlight(Entity):
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
        'total_impression_budget': int,
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

    def _construct_url(self, addl=None):
        # could use the SubEntity function but that breaks
        # if doing e.g. campaign.budget_flights[0].save()
        url = ['campaigns', str(self.campaign_id), self.collection]

        if self._init_properties.get('id'):
            url.append(str(self.id))
        if addl is not None:
            url.extend(addl)
        return '/'.join(url)

    def remove(self):
        """Remove a flight."""
        url = self._construct_url('delete')
        self._post(self._get_service_path(), rest=url, data={'version': self.version})
        for item in list(self._properties.keys()):
            del self._properties[item]
        for item in list(self._init_properties.keys()):
            del self._init_properties[item]
