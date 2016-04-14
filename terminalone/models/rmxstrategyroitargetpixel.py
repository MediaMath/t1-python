# -*- coding: utf-8 -*-
"""Provides RMX Strategy ROI Target Pixel object.
DEPRECATED: new entities should not be made.
"""

from __future__ import absolute_import
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
        'created_on': Entity._strpt,
        'id': int,
        'pixel_bundle_id': int,
        'price': float,
        'rmx_pixel_type': None,
        'rmx_strategy_id': int,
        'status': Entity._int_to_bool,
        'updated_on': Entity._strpt,
        'version': int,
    }

    def __init__(self, session, properties=None, **kwargs):
        super(RMXStrategyROITargetPixel, self).__init__(session,
                                                        properties, **kwargs)

    def save(self, *args, **kwargs):
        raise ClientError('This object is not editable.')
