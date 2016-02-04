# -*- coding: utf-8 -*-
"""Provides site list object."""

from __future__ import absolute_import
from ..entity import Entity


class SiteList(Entity):
    """Site list entity."""
    collection = 'site_lists'
    resource = 'site_list'
    _relations = {
        'organization',
    }
    _restrictions = Entity._enum({'INCLUDE', 'EXCLUDE'}, 'EXCLUDE')
    _pull = {
        'created_on': Entity._strpt,
        'filename': None,
        'id': int,
        'name': None,
        'organization_id': int,
        'restriction': None,
        'status': Entity._int_to_bool,
        'updated_on': Entity._strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'restriction': _restrictions,
        'status': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(SiteList, self).__init__(session, properties, **kwargs)
