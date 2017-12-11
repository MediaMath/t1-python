# -*- coding: utf-8 -*-
"""Provides retired audience segment object."""

from __future__ import absolute_import

from terminalone.errors import ClientError
from .. import t1types
from ..entity import Entity


class RetiredAudienceSegment(Entity):
    """Object for retired third-party segments."""
    collection = 'retired_audience_segments'
    resource = 'retired_audience_segment'
    _relations = {
        'audience_segment',
        'strategy',
    }
    _pull = {
        'buyable': t1types.int_to_bool,
        'wholesale_': t1types.strpt,
        'wholesale_cpm': float,
        'audience_vendor_id': int,
        'full_retired_path': None,
        'updated_on': t1types.strpt,
        'created_on': t1types.strpt,
        'id': int,
        'code': None,
        'version': int,
        'parent_audience_segment_id': int,
        'uniques': int,
        'type': None,

    }
    _push = _pull.copy()

    def __init__(self, session, properties=None, **kwargs):
        super(RetiredAudienceSegment, self).__init__(session, properties, **kwargs)

    def save(self, *args, **kwargs):
        raise ClientError('This object is not editable.')
