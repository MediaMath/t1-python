# -*- coding: utf-8 -*-
"""Provides strategy object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import T1Object

class T1Strategy(T1Object):
	"""docstring for T1Strategy."""
	collection = 'strategies'
	type = 'strategy'
	_aud_seg_exc = T1Object._enum({'AND', 'OR'}, 'OR')
	_aud_seg_inc = T1Object._enum({'AND', 'OR'}, 'OR')
	_freq_int = T1Object._enum({'hour', 'day', 'week', 'month', 'campaign',
					'not-applicable'}, 'not-applicable')
	_freq_type = T1Object._enum({'even', 'asap', 'no-limit'}, 'no-limit')
	_goal_type = T1Object._enum({'spend', 'reach', 'cpc', 'cpe', 'cpa', 'roi'},
								'cpc')
	_media_type = T1Object._enum({'DISPLAY', 'VIDEO'}, 'DISPLAY')
	_pac_int = T1Object._enum({'hour', 'day'}, 'day')
	_pac_type = T1Object._enum({'even', 'asap'}, 'even')
	_site_selec = T1Object._enum({'MATHSELECT_250', 'EXCLUDE_UGC', 'ALL',
								'REDUCED'}, 'REDUCED')
	_supply_type = T1Object._enum({'RTB', 'RMX_API', 'T1_RMX'}, 'RTB')
	_type = T1Object._enum({'REM', 'GBO', 'AUD'}, 'GBO')
	
	_pull = {
		'audience_segment_exclude_op': unicode,
		'audience_segment_include_op': unicode,
		'bid_aggresiveness': float,
		'bid_price_is_media_only': T1Object._int_to_bool,
		'budget': float,
		'campaign_id': int,
		'created_on': T1Object._strpt,
		'description': unicode,
		'end_date': T1Object._strpt,
		'feature_compatibility': unicode,
		'frequency_amount': int,
		'frequency_interval': unicode,
		'frequency_type': unicode,
		'goal_type': unicode,
		'goal_value': float,
		'id': int,
		'impression_cap': int,
		'max_bid': float,
		'media_type': unicode,
		'name': unicode,
		'pacing_amount': float,
		'pacing_interval': unicode,
		'pacing_type': unicode,
		'pixel_target_expr': unicode,
		'run_on_all_exchanges': T1Object._int_to_bool,
		'run_on_all_pmp': T1Object._int_to_bool,
		'run_on_dispaly': T1Object._int_to_bool,
		'run_on_mobile': T1Object._int_to_bool,
		'run_on_streaming': T1Object._int_to_bool,
		'site_restriction_transparent_urls': T1Object._int_to_bool,
		'site_selectiveness': unicode,
		'start_date': T1Object._strpt,
		'status': T1Object._int_to_bool,
		'supply_type': unicode,
		'type': unicode,
		'updated_on': T1Object._strpt,
		'use_campaign_end': T1Object._int_to_bool,
		'use_campaign_start': T1Object._int_to_bool,
		'use_mm_freq': T1Object._int_to_bool,
		'use_optimization': T1Object._int_to_bool,
		'version': int,
	}
	_push = _pull.copy()
	_push.update({
		'audience_segment_exclude_op': _aud_seg_exc,
		'audience_segment_include_op': _aud_seg_inc,
		'bid_price_is_media_only': int,
		'end_date': T1Object._strft,
		'frequency_interval': _freq_int,
		'frequency_type': _freq_type,
		'goal_type': _goal_type,
		'media_type': _media_type,
		'pacing_interval': _pac_int,
		'pacing_type': _pac_type,
		'run_on_all_exchanges': int,
		'run_on_all_pmp': int,
		'run_on_dispaly': int,
		'run_on_mobile': int,
		'run_on_streaming': int,
		'site_restriction_transparent_urls': int,
		'site_selectiveness': _site_selec,
		'start_date': T1Object._strft,
		'status': int,
		'supply_type': _supply_type,
		'type': _type,
		'use_campaign_end': int,
		'use_campaign_start': int,
		'use_mm_freq': int,
		'use_optimization': int,
	})
	_readonly = T1Object._readonly.copy()
	def __init__(self, auth, properties=None):
		super(T1Strategy, self).__init__(auth, properties)
