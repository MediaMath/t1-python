# -*- coding: utf-8 -*-
"""Provides publisher object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Publisher(Entity):
    """Publisher for PMP-D."""
    collection = 'publishers'
    resource = 'publisher'
    _relations = {
        'deal',
        'organization',
        'site',
    }
    _pull = {
        'created_on': t1types.strpt,
        'id': int,
        'name': None,
        'organization_id': int,
        'updated_on': t1types.strpt,
        'version': int,
    }
    _push = _pull

    def __init__(self, session, properties=None, **kwargs):
        super(Publisher, self).__init__(session, properties, **kwargs)
