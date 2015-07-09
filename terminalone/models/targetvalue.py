# -*- coding: utf-8 -*-
"""Provides region object."""

from __future__ import absolute_import
from ..errors import ClientError
from ..entity import Entity

class TargetValue(Entity):
    """docstring for TargetValue."""
    collection = 'target_values'
    resource = 'target_value'
    _relations = {
        'target_dimension',
    }

    _pull = {
        '_type': None,
        'code': None,
        'id': int,
        'is_targetable': Entity._int_to_bool,
        'name': None,
        'target_dimension_id': int,
        'value': int,
    }
    def __init__(self, session, properties=None, **kwargs):
        super(TargetValue, self).__init__(session, properties, **kwargs)

    def save(self, *args, **kwargs):
        raise ClientError('TargetValues are not editable.')
