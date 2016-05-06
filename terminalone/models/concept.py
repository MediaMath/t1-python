# -*- coding: utf-8 -*-
"""Provides concept object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Concept(Entity):
    """Concept entity."""
    collection = 'concepts'
    resource = 'concept'
    _relations = {
        'advertiser',
    }
    _pull = {
        'advertiser_id': int,
        'created_on': t1types.strpt,
        'id': int,
        'name': None,
        'status': t1types.int_to_bool,
        'updated_on': t1types.strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'status': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(Concept, self).__init__(session, properties, **kwargs)
