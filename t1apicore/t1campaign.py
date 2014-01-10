# -*- coding: utf-8 -*-
"""Provides campaign object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import T1Object

class T1Campaign(T1Object):
	"""docstring for T1Campaign.
	
	When creating a new campaign, "zone_name" must be """
	collection = 'campaigns'
	type = 'campaign'
	_relations = {
		'advertiser', 'ad_server', 'currency', 'merit_pixel', 'time_zone',
	}
	_conv = T1Object._enum({'every', 'one', 'variable'}, 'variable')
	_freq_ints = T1Object._enum({'hour', 'day', 'week', 'month',
								'not-applicable'}, 'not-applicable')
	_freq_types = T1Object._enum({'even', 'asap', 'no-limit'}, 'no-limit')
	_goal_cats = T1Object._enum({'audience', 'engagement', 'response'}, None)
	_goal_types = T1Object._enum({'spend', 'reach', 'cpc', 'cpe', 'cpa', 'roi'},
									None)
	_serv_types = T1Object._enum({'SELF', 'MANAGED'}, 'SELF')
	_pull = {
		'ad_server_fee': float,
		'ad_server_id': int,
		'ad_server_password': unicode,
		'ad_server_username': unicode,
		'advertiser_id': int,
		'agency_fee_pct': float,
		'conversion_type': unicode, # COME BACK HERE
		'conversion_variable_minutes': int,
		'created_on': T1Object._strpt,
		'currency_code': unicode,
		'end_date': T1Object._strpt,
		'frequency_amount': int,
		'frequency_interval': unicode,
		'frequency_type': unicode,
		'goal_alert': float,
		'goal_category': unicode,
		'goal_type': unicode,
		'goal_value': float,
		'has_custom_attribution': T1Object._int_to_bool,
		'id': int,
		'io_name': unicode,
		'io_reference_num': unicode,
		'margin_pct': float,
		'merit_pixel_id': int,
		'name': unicode,
		'pacing_alert': float,
		'pc_window_minutes': int,
		'pv_pct': float,
		'pv_window_minutes': int,
		'service_type': unicode,
		'spend_cap_amount': float,
		'spend_cap_automatic': T1Object._int_to_bool,
		'spend_cap_enabled': T1Object._int_to_bool,
		'start_date': T1Object._strpt,
		'status': T1Object._int_to_bool,
		'total_budget': float,
		'updated_on': T1Object._strpt,
		'use_default_ad_server': T1Object._int_to_bool,
		'use_mm_freq': T1Object._int_to_bool,
		'version': int,
		'zone_name': unicode,
	}
	_push = _pull.copy()
	_push.update({
		'conversion_type': _conv,
		'end_date': T1Object._strft,
		'frequency_interval': _freq_ints,
		'frequency_type': _freq_types,
		'goal_category': _goal_cats,
		'goal_type': _goal_types,
		'has_custom_attribution': int,
		'service_type': _serv_types,
		'spend_cap_automatic': int,
		'spend_cap_enabled': int,
		'start_date': T1Object._strft,
		'status': int,
		'use_default_ad_server': int,
		'use_mm_freq': int,
	})
	_readonly = T1Object._readonly.copy()
	def __init__(self, auth, properties=None):
		super(T1Campaign, self).__init__(auth, properties)
