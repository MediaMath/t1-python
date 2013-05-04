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
		self.writeable_attributes = {}
		# MORE ATTRIBUTES INCOMING??
		pass
		
		self.attribute_types = {'id': int, 'version': int, 'name': str, 'build_date': datetime,
			'created_on': datetime, 'updated_on': datetime, 'last_modified': datetime,
			'advertiser_id': int, 'concept_id': int, 'external_identifier': str,
			'file_type': str, 'tag_type': str, 'width': int, 'height': int,
			'is_https': str, 'has_sound': str, 'is_multi_creative': str,
			'ad_server_type': int, 'tag': str, 'tpas_ad_tag_name': str, 'status': str}
		
		self.conversion_funcs = {'id': int, 'version': int, 'name': str, 'build_date': self.dttp,
			'created_on': self.dttp, 'updated_on': self.dttp, 'last_modified': self.dttp,
			'advertiser_id': int, 'concept_id': int, 'external_identifier': str,
			'file_type': lambda x: x if str(x).lower() in frozenset(['gif', 'jpg', 'swf', 'unknown']) else 'unknown',
			'tag_type': lambda x: x if str(x).upper() in frozenset(['SCRIPT', 'IFRAME', 'NOSCRIPT']) else 'NOSCRIPT',
			'width': int, 'height': int, 'is_https': self.bool_deffalse,
			'has_sound': self.bool_deffalse, 'is_multi_creative': self.bool_deffalse,
			'ad_server_type': int, 'tag': str, 'tpas_ad_tag_name': str, 'status': self.bool_deftrue}
		
		pass
