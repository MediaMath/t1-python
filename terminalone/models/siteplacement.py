# -*- coding: utf-8 -*-
"""Provides site_placement object."""

from __future__ import absolute_import
from ..entity import Entity


class SitePlacement(Entity):
    """Site Placement for PMP-D."""
    collection = 'site_placements'
    resource = 'site_placement'
    _relations = {
        'publisher',
        'placement',
    }
    _deal_sources = Entity._enum({'USER', 'INTERNAL'}, 'USER')
    _media_types = Entity._enum({'display', 'video', 'mobile'}, 'display')
    _pmp_types = Entity._enum({'DIRECT', 'PREMIUM'}, 'DIRECT')
    _pull = {
        'bill_media_to_client': Entity._int_to_bool,
        'created_on': Entity._strpt,
        'deal_source': None,
        'display_text': None,
        'id': int,
        'media_type': None,
        'name': None,
        'pmp_type': None,
        'publisher_site_id': int,
        'updated_on': Entity._strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'bill_media_to_client': int,
        'deal_source': _deal_sources,
        'media_type': _media_types,
        'pmp_type': _pmp_types,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(SitePlacement, self).__init__(session, properties, **kwargs)

    def save(self, data=None, url=None):
        if data is None:
            data = self.properties
        if not data.get('display_text'):
            data['display_text'] = data['name']
        super(SitePlacement, self).save(data=data, url=url)
