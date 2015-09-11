# -*- coding: utf-8 -*-
"""Provides audience segment object."""

from __future__ import absolute_import
from ..entity import Entity


class AudienceSegment(Entity):
    """Audience segment entity object"""
    collection = 'audience_segments'
    resource = 'audience_segment'
    _relations = {
        'audience_vendor',
        'parent',
    }
    _pull = {
        'audience_vendor_id': int,
        'buyable': Entity._int_to_bool,
        'child_count': int,
        'code': None,
        'created_on': Entity._strpt,
        'full_path': None,
        'id': int,
        'name': None,
        'parent_audience_segment_id': int,
        'retail_cpm': float,
        'wholesale_cpm': float,
        'tag': None,
        'uniques': int,
        'updated_on': Entity._strpt,
        'version': int,
    }

    _push = _pull.copy()
    _push.update({
        'buyable': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(AudienceSegment, self).__init__(session, properties, **kwargs)
