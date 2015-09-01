# -*- coding: utf-8 -*-
"""Provides vendor object."""

from __future__ import absolute_import
from ..entity import Entity


class Vendor(Entity):
    """Provides vendor entity."""
    collection = 'vendors'
    resource = 'vendor'
    _relations = {
        'vendor_contracts',
        'vendor_domains',
    }
    # _rate_card_types = Entity._enum({'CPM', 'FIXED'}, None)
    _vendor_types = Entity._enum({'AD_SERVER', 'AD_VERIFICATION', 'CONTEXTUAL',
                                  'DATA', 'DSP', 'DYNAMIC_CREATIVE', 'NETWORK',
                                  'OBA_COMPLIANCE', 'OTHER', 'PIXEL_TRACKING',
                                  'RICH_MEDIA', 'SURVEY'}, 'OTHER')
    _pull = {
        'adx_approved': Entity._int_to_bool,
        'adx_declaration_required': Entity._int_to_bool,
        'adx_ssl_approved': Entity._int_to_bool,
        'adx_vendor_identifier': None,
        'adx_video_approved': Entity._int_to_bool,
        'adx_video_ssl_approved': Entity._int_to_bool,
        'created_on': Entity._strpt,
        'description': None,
        'id': int,
        'is_eligible': Entity._int_to_bool,
        'mm_contract_available': Entity._int_to_bool,
        'name': None,
        'rate_card_price': float,
        'rate_card_type': None,
        'updated_on': Entity._strpt,
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
