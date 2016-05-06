# -*- coding: utf-8 -*-
"""Provides target value object."""

from __future__ import absolute_import
from .. import t1types
from ..errors import ClientError
from ..entity import Entity


class TargetValue(Entity):
    """Target value value and target value count entities"""
    collection = 'target_values'
    resource = 'target_value'
    _relations = {
        'target_dimension',
    }

    _pull = {
        '_type': None,
        'child_count': int,
        'code': None,
        'dimension_code': None,
        'id': int,
        'is_targetable': t1types.int_to_bool,
        'name': None,
        'target_dimension_id': int,
        'value': int,
    }

    def __init__(self, session, properties=None, **kwargs):
        super(TargetValue, self).__init__(session, properties, **kwargs)

    def save(self, *args, **kwargs):
        raise ClientError('TargetValues are not editable.')
