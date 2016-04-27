# -*- coding: utf-8 -*-
"""Provides advertiser object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Advertiser(Entity):
    """Advertiser entity."""
    collection = 'advertisers'
    resource = 'advertiser'
    _dmp_settings = t1types.enum({'disabled', 'inherits'}, 'inherits')
    _freq_int = t1types.enum({'hour', 'day', 'week', 'month', 'campaign',
                              'not-applicable'}, 'not-applicable')
    _freq_type = t1types.enum({'even', 'asap', 'no-limit'}, 'no-limit')
    _relations = {
        'ad_server', 'agency', 'billing_contact', 'sales_contact', 'vertical',
    }
    _pull = {
        'ad_server_fee': float,
        'ad_server_id': int,
        'ad_server_password': None,
        'ad_server_username': None,
        'agency_id': int,
        'allow_x_strat_optimization': t1types.int_to_bool,
        'billing_contact_id': int,
        'created_on': t1types.strpt,
        'domain': None,
        'dmp_enabled': None,
        'frequency_amount': int,
        'frequency_interval': None,
        'frequency_type': None,
        'id': int,
        'minimize_multi_ads': t1types.int_to_bool,
        'name': None,
        'sales_contact_id': int,
        'status': t1types.int_to_bool,
        'updated_on': t1types.strpt,
        'version': int,
        'vertical_id': int,
    }
    _push = _pull.copy()
    _push.update({
        'allow_x_strat_optimization': int,
        'frequency_interval': _freq_int,
        'frequency_type': _freq_type,
        'minimize_multi_ads': int,
        'status': int,
        'dmp_enabled': _dmp_settings,

    })

    def __init__(self, session, properties=None, **kwargs):
        super(Advertiser, self).__init__(session, properties, **kwargs)
