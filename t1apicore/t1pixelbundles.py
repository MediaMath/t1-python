# -*- coding: utf-8 -*-
"""Provides Pixel Bundles object for working with creatives.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from t1object import T1Object
# IMPORT

class T1PixelBundles(T1Object):
	"""docstring for T1PixelBundles"""
	def __init__(self):
		super(T1PixelBundles, self).__init__()
		del self._types['status']
		del self._convert['status']
		self.collection = 'pixel_bundles'
		self.data_only = {'agency_id', 'pricing', 'cost_pct_cpm',
							'cost_cpts', 'cost_cpm'}
		self.event_only = {'advertiser_id'}
		self._readonly.update({'pixel_type', 'tags', 'external_identifier',
								'tag_type'})
		self._types.update({'advertiser_id': int, 'agency_id': int, 'tag_type': str,
			'external_identifier': str, 'keywords': str, 'eligible': str,
			'pixel_type': str, 'provider_id': int, 'pricing': str,
			'cost_cpts': str, 'cost_pct_cpm': str, 'cost_cpm': str})
		self._convert.update({'advertiser_id': int, 'agency_id': int,
			'pixel_type': lambda x: x if x in frozenset(['event', 'data']) else 'event',
			'tag_type': lambda x: x if x in frozenset(['image', 'js', 'dfa', 'uat']) else 'image',
			'provider_id': int, 'pricing': None,
			pass}
		
		pass
