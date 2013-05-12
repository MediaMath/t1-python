# -*- coding: utf-8 -*-
"""Provides Atomic Creative object for working with creatives.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from t1object import T1Object
# IMPORT

class T1AtomicCreative(T1Object):
	"""docstring for T1AtomicCreative"""
	def __init__(self):
		super(T1AtomicCreative, self).__init__()
		self.collection = 'atomic_creatives'
		self._readonly.update({'t1as'})
		self._types.update({'advertiser_id': int, 'concept_id': int,
			'external_identifier': str, 'file_type': str, 'tag_type': str,
			'width': int, 'height': int, 'is_https': str, 'has_sound': str,
			'is_multi_creative': str, 'ad_server_type': int, 'tag': str,
			'tpas_ad_tag_name': str, 'edited_tag': str, 'tpas_ad_tag': str})
		
		self._convert.update({'advertiser_id': int, 'concept_id': int,
			'file_type': lambda x: x if str(x) in frozenset(['gif', 'jpg', 'swf', 'unknown']) else 'unknown',
			'tag_type': lambda x: x if str(x) in frozenset(['SCRIPT', 'IFRAME', 'NOSCRIPT']) else 'NOSCRIPT',
			'width': int, 'height': int, 'is_https': self._bool_deffalse, 'external_identifier': str,
			'has_sound': self._bool_deffalse, 'is_multi_creative': self._bool_deffalse,
			'ad_server_type': int, 'tag': str, 'tpas_ad_tag_name': str,
			'edited_tag': str, 'tpas_ad_tag': str})
		
		pass
