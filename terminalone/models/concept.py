# -*- coding: utf-8 -*-
"""Provides concept object."""

from __future__ import absolute_import
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
        'created_on': Entity._strpt,
        'id': int,
        'name': None,
        'status': Entity._int_to_bool,
        'updated_on': Entity._strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'status': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(Concept, self).__init__(session, properties, **kwargs)
