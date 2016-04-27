# -*- coding: utf-8 -*-
"""Provides campaign object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Campaign(Entity):
    """Campaign entity.

    When creating a new campaign, "zone_name" must be set to the name, such as
    America/New_York, rather than the code. A list of time zone names can be
    found on the developer portal."""
    collection = 'campaigns'
    resource = 'campaign'
    _relations = {
        'advertiser', 'ad_server', 'currency', 'merit_pixel', 'time_zone',
    }
    _conv = t1types.enum({'every', 'one', 'variable'}, 'variable')
    _freq_ints = t1types.enum({'hour', 'day', 'week', 'month',
                               'not-applicable'}, 'not-applicable')
    _freq_types = t1types.enum({'even', 'asap', 'no-limit'}, 'no-limit')
    _goal_cats = t1types.enum({'audience', 'engagement', 'response'}, None)
    _goal_types = t1types.enum({'spend', 'reach', 'cpc', 'cpe', 'cpa', 'roi'},
                               None)
    _serv_types = t1types.enum({'SELF', 'MANAGED'}, 'SELF')
    _pull = {
        'ad_server_fee': float,
        'ad_server_id': int,
        'ad_server_password': None,
        'ad_server_username': None,
        'advertiser_id': int,
        'agency_fee_pct': float,
        'conversion_type': None,
        'conversion_variable_minutes': int,
        'created_on': t1types.strpt,
        'currency_code': None,
        'dcs_data_is_campaign_level': t1types.int_to_bool,
        'end_date': t1types.strpt,
        'frequency_amount': int,
        'frequency_interval': None,
        'frequency_type': None,
        'goal_alert': float,
        'goal_category': None,
        'goal_type': None,
        'goal_value': float,
        'has_custom_attribution': t1types.int_to_bool,
        'id': int,
        'io_name': None,
        'io_reference_num': None,
        'initial_start_date': t1types.strpt,
        'margin_pct': float,
        'merit_pixel_id': int,
        'name': None,
        'pacing_alert': float,
        'pc_window_minutes': int,
        'pv_pct': float,
        'pv_window_minutes': int,
        'service_type': None,
        'spend_cap_amount': float,
        'spend_cap_automatic': t1types.int_to_bool,
        'spend_cap_enabled': t1types.int_to_bool,
        'start_date': t1types.strpt,
        'status': t1types.int_to_bool,
        'total_budget': float,
        'updated_on': t1types.strpt,
        'use_default_ad_server': t1types.int_to_bool,
        'use_mm_freq': t1types.int_to_bool,
        'version': int,
        'zone_name': None,
    }
    _push = _pull.copy()
    _push.update({
        'conversion_type': _conv,
        'dcs_data_is_campaign_level': int,
        'end_date': t1types.strft,
        'frequency_interval': _freq_ints,
        'frequency_type': _freq_types,
        'goal_category': _goal_cats,
        'goal_type': _goal_types,
        'has_custom_attribution': int,
        'initial_start_date': t1types.strft,
        'service_type': _serv_types,
        'spend_cap_automatic': int,
        'spend_cap_enabled': int,
        'start_date': t1types.strft,
        'status': int,
        'use_default_ad_server': int,
        'use_mm_freq': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(Campaign, self).__init__(session, properties, **kwargs)
