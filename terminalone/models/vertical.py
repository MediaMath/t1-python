# -*- coding: utf-8 -*-
"""Provides vertical object."""

from __future__ import absolute_import
from ..entity import Entity


class Vertical(Entity):
    """docstring for Vertical."""
    collection = 'verticals'
    resource = 'vertical'
    _relations = {
        'advertiser',
    }

    _pull = {
        'id': int,
        'name': None,
        'created_on': Entity._strpt,
        'updated_on': Entity._strpt,
        'version': int,
    }

    _push = _pull

    def __init__(self, session, properties=None, **kwargs):
        super(Vertical, self).__init__(session, properties, **kwargs)
