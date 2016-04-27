# -*- coding: utf-8 -*-
"""Provides RMX Strategy object. DEPRECATED: new entities should not be made."""

from __future__ import absolute_import
from warnings import warn
from .. import t1types
from ..entity import Entity
from ..errors import ClientError


class RMXStrategy(Entity):
    """RMXStrategy entity. DEPRECATED: new entities should not be made."""
    collection = 'rmx_strategies'
    resource = 'rmx_strategy'
    _relations = {
        'pixel_bundle', 'strategy', 'rmx_strategy_roi_target_pixels'
    }
    _pull = {
        'budget': float,
        'budget_type': None,
        'cpa_pixel_bundle_id': int,
        'cpa_pixel_type': None,
        'created_on': t1types.strpt,
        'dynamic_pricing_option': None,
        'id': int,
        'imp_budget': float,
        'learning_budget': float,
        'learning_budget_pacing': None,
        'learning_slider': float,
        'pacing': None,
        'price': float,
        'pricing_type': None,
        'rmx_push_entity_id': int,
        'rmx_push_status': None,
        'rmxapi_io_identifier': int,
        'rmxapi_li_identifier': int,
        'roi_cpc_target_ctr': float,
        'roi_cpc_target_ctr_type': None,
        'roi_modifier': float,
        'roi_targets': None,
        'status': t1types.int_to_bool,
        'strategy_id': int,
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
        super(RMXStrategy, self).__init__(session, properties, **kwargs)

    def save(self, *args, **kwargs):
        raise ClientError('This object is not editable.')
