# -*- coding: utf-8 -*-
"""Provides strategy concept object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class StrategyConcept(Entity):
    """StrategyConcept object to join strategy and concept."""
    collection = 'strategy_concepts'
    resource = 'strategy_concept'
    _relations = {
        'concept',
        'strategy',
    }
    _weight_types = t1types.enum({'IMPRESSION', 'BUDGET', 'NONE'}, 'NONE')
    _pull = {
        'concept_id': int,
        'created_on': t1types.strpt,
        'id': int,
        'percent': float,
        'status': t1types.int_to_bool,
        'strategy_id': int,
        'updated_on': t1types.strpt,
        'version': int,
        'weighting': None,
    }
    _push = _pull.copy()
    _push.update({
        'status': int,
        'weighting': _weight_types,
    })
    _readonly = Entity._readonly | {'name', }

    def __init__(self, session, properties=None, **kwargs):
        super(StrategyConcept, self).__init__(session, properties, **kwargs)

    def remove(self):
        """Unassign the concept from the strategy."""
        url = '/'.join([self.collection,
                        str(self.id),
                        'delete'])
        self._post(self._get_service_path(), rest=url, data={'version': self.version})
        for item in list(self._properties.keys()):
            del self._properties[item]
