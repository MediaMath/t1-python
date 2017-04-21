# -*- coding: utf-8 -*-
"""Provides child pixel object. This is *distinct* from PixelBundle; please see the documentation"""

from __future__ import absolute_import

from .. import t1types
from ..entity import Entity


class ChildPixel(Entity):
    """Child pixel (i.e. piggybacked) entity."""
    collection = 'pixels'
    resource = 'pixel'
    _relations = {
        'pixel_bundle',
    }
    _pixel_types = t1types.enum({'creative', 'event', 'data'}, None)
    _pull = {
        'bundle_id': int,
        'created_on': t1types.strpt,
        'distributed': t1types.int_to_bool,
        'id': int,
        'pixel_type': None,
        'supply_source_id': int,
        'tag': None,
        'updated_on': t1types.strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'distributed': int,
        'pixel_type': _pixel_types,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(ChildPixel, self).__init__(session, properties, **kwargs)

    def remove(self):
        """Remove the pixel from the container."""
        url = '/'.join([self.collection,
                        str(self.id),
                        'delete'])
        self._post(self._get_service_path(), rest=url, data={'version': self.version})
        for item in list(self._properties.keys()):
            del self._properties[item]
