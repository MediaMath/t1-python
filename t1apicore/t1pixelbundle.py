# -*- coding: utf-8 -*-
"""Provides Pixel Bundles object for working with creatives.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import T1Object
# IMPORT

class T1PixelBundle(T1Object):
	"""docstring for T1PixelBundle"""
	collection = 'pixel_bundles'
	type = 'pixel_bundle'
	_pixel_types = T1Object._enum({'creative', 'event', 'data', 'segment'},
									'event')
	_pricing = T1Object._enum({'CPM', 'CPTS'}, 'CPM')
	_rmx_conv_types = T1Object._enum({'one', 'variable'}, 'one')
	_tag_types = T1Object._enum({'dfa', 'uat', 'image', 'iframe', 'js'}, 'image')
	_pull = {
		'advertiser_id': int,
		'agency_id': int,
		'cost_cpm': float,
		'cost_cpts': float,
		'cost_pct_cpm': float,
		'created_on': T1Object._strpt,
		'eligible': T1Object._int_to_bool,
		'external_identifier': str,
		'id': int,
		'name': str,
		'pixel_type': str,
		'pricing': str,
		'provider_id': int,
		'rmx_conversion_minutes': int,
		'rmx_conversion_type': str,
		'rmx_friendly': T1Object._int_to_bool,
		'rmx_merit': T1Object._int_to_bool,
		'rmx_pc_window_minutes': int,
		'rmx_pv_window_minutes': int,
		'segment_op': str,
		'tag_type': str,
		'tags': str,
		'type': 'pixel_bundle',
		'updated_on': T1Object._strpt,
		'version': int,
	}
	_push = _pull.copy()
	_push.update({
		'eligible': int,
		'pixel_type': _pixel_types,
		'pricing': _pricing,
		'rmx_conversion_type': _rmx_conv_types,
		'rmx_friendly': int,
		'rmx_merit': int,
		'tag_type': _tag_types,
	})
	_readonly = T1Object._readonly.copy()
	_readonly.update({'tags', 'external_identifier',})
	def __init__(self, auth, properties=None):
		super(T1PixelBundle, self).__init__(auth, properties)
		pass
