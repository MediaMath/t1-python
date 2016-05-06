# -*- coding: utf-8 -*-
"""Provides strategy concept object."""

from __future__ import absolute_import
from .. import t1types
from ..config import PATHS
from ..entity import Entity


class StrategyConcept(Entity):
    """docstring for StrategyConcept."""
    collection = 'strategy_concepts'
    resource = 'strategy_concept'
    _relations = {
        'concept',
        'strategy',
    }
    _pull = {
        'concept_id': int,
        'created_on': t1types.strpt,
        'id': int,
        'status': t1types.int_to_bool,
        'strategy_id': int,
        'updated_on': t1types.strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'status': int,
    })
    _readonly = Entity._readonly | {'name', }

    def __init__(self, session, properties=None, **kwargs):
        super(StrategyConcept, self).__init__(session, properties, **kwargs)

    def remove(self):
        """Unassign the concept from the strategy."""
        url = '/'.join([self.collection,
                        str(self.id),
                        'delete'])
        self._post(PATHS['mgmt'], rest=url, data={'version': self.version})
        for item in list(self.properties.keys()):
            del self.properties[item]
