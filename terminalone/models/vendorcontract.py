# -*- coding: utf-8 -*-
"""Provides vendor_contract object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class VendorContract(Entity):
    """Provides vendor contract entity."""
    collection = 'vendor_contracts'
    resource = 'vendor_contract'
    _relations = {
        'campaign',
        'vendor',
    }
    _pull = {
        'campaign_id': int,
        'created_on': t1types.strpt,
        'id': int,
        'price': float,
        'rate_card_type': None,
        'updated_on': t1types.strpt,
        'use_mm_contract': t1types.int_to_bool,
        'vendor_id': int,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'use_mm_contract': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(VendorContract, self).__init__(session, properties, **kwargs)
