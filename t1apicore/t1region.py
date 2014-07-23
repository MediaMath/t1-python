# -*- coding: utf-8 -*-
"""Provides region object.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import T1Object

class T1Region(T1Object):
	"""docstring for T1Region."""
	collection = 'regions'
	type = 'region'
	_relations = {
		'target_dimension',
	}
	# _aud_seg_exc = T1Object._enum({'AND', 'OR'}, 'OR')
	# _aud_seg_inc = T1Object._enum({'AND', 'OR'}, 'OR')
	# _freq_int = T1Object._enum({'hour', 'day', 'week', 'month', 'campaign',
	# 				'not-applicable'}, 'not-applicable')
	# _freq_type = T1Object._enum({'even', 'asap', 'no-limit'}, 'no-limit')
	# _goal_type = T1Object._enum({'spend', 'reach', 'cpc', 'cpe', 'cpa', 'roi'},
	# 							'cpc')
	# _media_type = T1Object._enum({'DISPLAY', 'VIDEO'}, 'DISPLAY')
	# _pac_int = T1Object._enum({'hour', 'day'}, 'day')
	# _pac_type = T1Object._enum({'even', 'asap'}, 'even')
	# _site_selec = T1Object._enum({'MATHSELECT_250', 'EXCLUDE_UGC', 'ALL',
	# 							'REDUCED'}, 'REDUCED')
	# _supply_type = T1Object._enum({'RTB', 'RMX_API', 'T1_RMX'}, 'RTB')
	# _type = T1Object._enum({'REM', 'GBO', 'AUD'}, 'GBO')
	
	_pull = {
		'_type': None,
		'code': None,
		'id': int,
		'is_targetable': T1Object._int_to_bool,
		'name': None,
		'target_dimension_id': int,
		'value': int,
	}
	_push = _pull.copy()
	_push.update({
		'is_targetable': int,
	})
	_readonly = T1Object._readonly.copy()
	def __init__(self, session, properties=None, **kwargs):
		super(T1Region, self).__init__(session, properties, **kwargs)

	def save(self):
		raise T1ClientError('T1Regions are not editable.')
