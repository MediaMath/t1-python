# -*- coding: utf-8 -*-
"""Provides vendor object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Vendor(Entity):
    """Provides vendor entity."""
    collection = 'vendors'
    resource = 'vendor'
    _relations = {
        'vendor_contracts',
        'vendor_domains',
    }
    # _rate_card_types = t1types.enum({'CPM', 'FIXED'}, None)
    _vendor_types = t1types.enum({'AD_SERVER', 'AD_VERIFICATION', 'CONTEXTUAL',
                                  'DATA', 'DSP', 'DYNAMIC_CREATIVE', 'NETWORK',
                                  'OBA_COMPLIANCE', 'OTHER', 'PIXEL_TRACKING',
                                  'RICH_MEDIA', 'SURVEY'}, 'OTHER')
    _pull = {
        'adx_approved': t1types.int_to_bool,
        'adx_declaration_required': t1types.int_to_bool,
        'adx_ssl_approved': t1types.int_to_bool,
        'adx_vendor_identifier': None,
        'adx_video_approved': t1types.int_to_bool,
        'adx_video_ssl_approved': t1types.int_to_bool,
        'created_on': t1types.strpt,
        'description': None,
        'id': int,
        'is_eligible': t1types.int_to_bool,
        'mm_contract_available': t1types.int_to_bool,
        'name': None,
        'rate_card_price': float,
        'rate_card_type': None,
        'updated_on': t1types.strpt,
        'vendor_type': None,
        'version': int,
        'wholesale_price': float,
    }
    _push = _pull.copy()
    _push.update({
        'adx_approved': int,
        'adx_declaration_required': int,
        'adx_ssl_approved': int,
        'adx_video_approved': int,
        'adx_video_ssl_approved': int,
        'is_eligible': int,
        'mm_contract_available': int,
        'vendor_type': _vendor_types,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(Vendor, self).__init__(session, properties, **kwargs)
