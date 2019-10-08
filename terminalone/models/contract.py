# -*- coding: utf-8 -*-
"""Provides contract object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Contract(Entity):
    """Provides contract entity."""
    collection = 'contracts'
    resource = 'contract'
    _relations = {
        'organization'
    }
    _pull = {
        'organization_id': int,
        'effective_start_date': t1types.strpt,
        'effective_end_date': t1types.strpt,
        'created_on': t1types.strpt,
        'id': int,
        'updated_on': t1types.strpt,
        'version': int,
    }

    def __init__(self, session, properties=None, **kwargs):
        super(Contract, self).__init__(session, properties, **kwargs)
