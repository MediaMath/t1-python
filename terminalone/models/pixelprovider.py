# -*- coding: utf-8 -*-
"""Provides pixel provider object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class PixelProvider(Entity):
    """docstring for pixel provider."""
    collection = 'pixel_providers'
    resource = 'pixel_provider'
    _executors = t1types.enum({'MEDIAMATH', 'UDI'}, 'UDI')
    _relations = {
        'agency',
        'vendor',
    }
    _pull = {
        'agency_id': int,
        'created_on': t1types.strpt,
        'execution_by': None,
        'id': int,
        'name': None,
        'status': t1types.int_to_bool,
        'taxonomy_file': None,
        'updated_on': t1types.strpt,
        'vendor_id': int,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'execution_by': _executors,
        'status': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(PixelProvider, self).__init__(session, properties, **kwargs)
