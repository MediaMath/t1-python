# -*- coding: utf-8 -*-
"""Provides RMX Strategy ROI Target Pixel object.
DEPRECATED: new entities should not be made.
"""

from __future__ import absolute_import
from warnings import warn
from .. import t1types
from ..entity import Entity
from ..errors import ClientError


class RMXStrategyROITargetPixel(Entity):
    """RMXStrategyROITargetPixel entity.
    DEPRECATED: new entities should not be made.
    """
    collection = 'rmx_strategy_roi_target_pixels'
    resource = 'rmx_strategy_roi_target_pixel'
    _relations = {
        'pixel_bundle', 'rmx_strategy'
    }
    _pull = {
        'created_on': t1types.strpt,
        'id': int,
        'pixel_bundle_id': int,
        'price': float,
        'rmx_pixel_type': None,
        'rmx_strategy_id': int,
        'status': t1types.int_to_bool,
        'updated_on': t1types.strpt,
        'version': int,
    }

    def __init__(self, session, properties=None, **kwargs):
        if properties is None:
            # stacklevel=3 means that the line that called t1.new will be
            # shown to the user. stacklevel=2 will just show the initialization,
            # not the line that called for the instantiation.
            warn('Deprecated entity: this entity is only included for certain '
                 'strategies that automatically include it. New instances '
                 'should not be created.', UserWarning, stacklevel=3)
        super(RMXStrategyROITargetPixel, self).__init__(session,
                                                        properties, **kwargs)

    def save(self, *args, **kwargs):
        raise ClientError('This object is not editable.')
