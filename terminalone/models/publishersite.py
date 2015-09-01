# -*- coding: utf-8 -*-
"""Provides publisher_site object."""

from __future__ import absolute_import
from ..entity import Entity


class PublisherSite(Entity):
    """Publisher Site for PMP-D."""
    collection = 'publisher_sites'
    resource = 'publisher_site'
    _relations = {
        'publisher',
        'placement',
    }
    _pull = {
        'created_on': Entity._strpt,
        'id': int,
        'name': None,
        'publisher_id': int,
        'updated_on': Entity._strpt,
        'version': int,
    }
    _push = _pull

    def __init__(self, session, properties=None, **kwargs):
        super(PublisherSite, self).__init__(session, properties, **kwargs)
