# -*- coding: utf-8 -*-
"""Provides site list object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class SiteList(Entity):
    """Site list entity."""
    collection = 'site_lists'
    resource = 'site_list'
    _relations = {
        'organization',
    }
    _restrictions = t1types.enum({'INCLUDE', 'EXCLUDE'}, 'EXCLUDE')
    _pull = {
        'created_on': t1types.strpt,
        'filename': None,
        'id': int,
        'name': None,
        'organization_id': int,
        'restriction': None,
        'status': t1types.int_to_bool,
        'updated_on': t1types.strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'restriction': _restrictions,
        'status': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(SiteList, self).__init__(session, properties, **kwargs)
