# -*- coding: utf-8 -*-
"""Provides child pixel object. This is *distinct* from PixelBundle; please see the documentation"""

from __future__ import absolute_import
from ..entity import Entity


class ChildPixel(Entity):
    """docstring for child pixel."""
    collection = 'pixels'
    resource = 'pixel'
    _relations = {
        'pixel_bundle',
    }
    _pixel_types = Entity._enum({'creative', 'event', 'data'}, None)
    _pull = {
        'bundle_id': int,
        'created_on': Entity._strpt,
        'distributed': Entity._int_to_bool,
        'id': int,
        'pixel_type': None,
        'supply_source_id': int,
        'tag': None,
        'updated_on': Entity._strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'distributed': int,
        'pixel_type': _pixel_types,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(ChildPixel, self).__init__(session, properties, **kwargs)
