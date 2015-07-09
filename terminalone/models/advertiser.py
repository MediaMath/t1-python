# -*- coding: utf-8 -*-
"""Provides advertiser object."""

from __future__ import absolute_import
from ..entity import Entity

class Advertiser(Entity):
    """docstring for Advertiser"""
    collection = 'advertisers'
    resource = 'advertiser'
    _relations = {
        'ad_server', 'agency', 'billing_contact', 'sales_contact', 'vertical',
    }
    _pull = {
        'ad_server_fee': float,
        'ad_server_id': int,
        'ad_server_password': None,
        'ad_server_username': None,
        'agency_id': int,
        'allow_x_strat_optimization': Entity._int_to_bool,
        'billing_contact_id': int,
        'created_on': Entity._strpt,
        'domain': None,
        'id': int,
        'minimize_multi_ads': Entity._int_to_bool,
        'name': None,
        'sales_contact_id': int,
        'status': Entity._int_to_bool,
        'updated_on': Entity._strpt,
        'version': int,
        'vertical_id': int,
    }
    _push = _pull.copy()
    _push.update({
        'allow_x_strat_optimization': int,
        'minimize_multi_ads': int,
        'status': int,
    })
    def __init__(self, session, properties=None, **kwargs):
        super(Advertiser, self).__init__(session, properties, **kwargs)
