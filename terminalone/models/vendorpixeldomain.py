# -*- coding: utf-8 -*-
"""Provides vendor_pixel_domain object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class VendorPixelDomain(Entity):
    """Provides vendor pixel entity."""
    collection = 'vendor_pixel_domains'
    resource = 'vendor_pixel_domain'
    _relations = {
        'creative',
        'vendor_domain',
        'vendor_pixel',
    }
    _pull = {
        'created_on': t1types.strpt,
        'domain': None,
        'id': int,
        'vendor_domain_id': int,
        'vendor_pixel_id': int,
        'version': int,
    }
    _push = _pull

    def __init__(self, session, properties=None, **kwargs):
        super(VendorPixelDomain, self).__init__(session, properties, **kwargs)
