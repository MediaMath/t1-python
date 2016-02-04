# -*- coding: utf-8 -*-
"""Provides ad server object."""

from __future__ import absolute_import
from ..entity import Entity


class AdServer(Entity):
    """Ad Server entity."""
    collection = 'ad_servers'
    resource = 'ad_server'
    _relations = set()
    _pull = {
        'id': int,
        'name': None,
        'version': int,
    }
    _push = _pull

    def __init__(self, session, properties=None, **kwargs):
        super(AdServer, self).__init__(session, properties, **kwargs)
