# -*- coding: utf-8 -*-
"""Provides Pixel Bundles object for working with creatives.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import *
# IMPORT

class T1PixelBundles(T1Object):
	"""docstring for T1PixelBundles"""
	def __init__(self):
		super(T1PixelBundles, self).__init__()
		del self._types['status']
		del self._convert['status']
		self.collection = 'pixel_bundles'
		self._readonly.update({'pixel_type', 'tags', 'external_identifier',
								'tag_type'})
		self._pixel_types = self._enum({'creative', 'event', 'data', 'segment'},
										'event')
		self._pricing = self._enum({'CPM', 'CPTS'}, 'CPM')
		self._rmx_conv_types = self._enum({'one', 'variable'}, 'one')
		self._tag_types = self._enum({'dfa', 'uat', 'image', 'iframe', 'js'},
										'image')
		self._pull.update({
			'advertiser_id': int,
			'agency_id': int,
			'cost_cpm': float,
			'cost_cpts': float,
			'cost_pct_cpm': float,
			'eligible': self._int_to_bool,
			'external_identifier': str,
			'pixel_type': str,
			'pricing': str,
			'provider_id': int,
			'rmx_conversion_minutes': int,
			'rmx_conversion_type': str,
			'rmx_friendly': self._int_to_bool,
			'rmx_merit': self._int_to_bool,
			'rmx_pc_window_minutes': int,
			'rmx_pv_window_minutes': int,
			'segment_op': str,
			'tag_type': str,
			'tags': str,
		})
		self._push = self._pull.copy()
		self._push.update({
			'eligible': int,
			'pixel_type': self._pixel_types,
			'pricing': self._pricing,
			'rmx_conversion_type': self._rmx_conv_types,
			'rmx_friendly': int,
			'rmx_merit': int,
			'tag_type': str,
		})
		
		pass
