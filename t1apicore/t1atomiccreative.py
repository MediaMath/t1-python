# -*- coding: utf-8 -*-
"""Provides Atomic Creative object for working with creatives.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from t1object import T1Object
from datetime import datetime
# IMPORT

class T1AtomicCreative(T1Object):
	"""docstring for T1AtomicCreative"""
	def __init__(self):
		super(T1AtomicCreative, self).__init__()
		self.collection = 'atomic_creatives'
		self._ad_formats = self._valid_enum(frozenset(['DISPLAY', 'EXPANDABLE', 'MOBILE']), 'DISPLAY')
		self._ad_servers = self._valid_enum(frozenset(['ATLAS', 'DART', 'EYEWONDER', 'MEDIAMIND',
									'MEDIAPLEX', 'POINTROLL', 'YIELD_MANAGER',
									'TERMINALONE', 'MEDIAFORGE', 'OTHER']), 'OTHER')
		self._approved = self._valid_enum(frozenset(['PENDING', 'APPROVED', 'REJECTED']), 'PENDING')
		self._expand_dir = self._valid_enum(frozenset(['L', 'R', 'U', 'D', 'LD', 'RD', 'LU',
											'RU', 'NONRESTRICTED']), 'NONRESTRICTED')
		self._expand_trig = self._valid_enum(frozenset(['AUTOMATIC', 'MOUSEOVER', 'CLICK']), 'CLICK')
		self._file_types = self._valid_enum(frozenset(['gif', 'jpg', 'swf', 'unknown']), 'unkown')
		self._tag_types = self._valid_enum(frozenset(['SCRIPT', 'IFRAME', 'NOSCRIPT']), 'NOSCRIPT')
		self._readonly.update({'t1as'})
		self._types.update({'advertiser_id': int, 'concept_id': int,
			'external_identifier': str, 'file_type': str, 'tag_type': str,
			'width': int, 'height': int, 'is_https': str, 'has_sound': str,
			'is_multi_creative': str, 'ad_server_type': str, 'tag': str,
			'tpas_ad_tag_name': str, 'edited_tag': str, 'tpas_ad_tag': str,
			'ad_format': str, 'approval_status': str, 'build_errors': str,
			'built': bool, 'built_by_user_id': int, 'click_through_url': str,
			'click_url': str, 'creative_import_file_id': int, 'end_date': datetime,
			'expansion_direction': str, 'expansion_trigger': str, 'rejected_reason': str,
			'rich_media': bool, 'rich_media_provider': str, 'start_date': datetime,
			't1as': bool
			})
		self._convert_lambda = lambda x, y, z: x if str(x) in y else z
		# What I really want here is a closure. Want to freeze y and z when I assign
		# in _convert, and x is what gets passed on function call
		self._convert.update({'advertiser_id': int, 'concept_id': int,
			'file_type': self._file_types, 'tag_type': self._tag_types,
			'ad_format': self._ad_formats, 'ad_server_type': self._ad_servers,
			'width': int, 'height': int, 'is_https': self._bool_deffalse, 'external_identifier': str,
			'has_sound': self._bool_deffalse, 'is_multi_creative': self._bool_deffalse,
			'tag': str, 'tpas_ad_tag_name': str,
			'edited_tag': str, 'tpas_ad_tag': str, 'approval_status': self._approved,
			'build_errors': str, 'built': self._int_to_bool, 'built_by_user_id': int,
			'click_through_url': str, 'click_url': str, 'creative_import_file_id': int,
			'end_date': self._strpt, 'expansion_direction': self._expand_dir,
			'expansion_trigger': self._expand_trig, 'rejected_reason': str,
			'rich_media': self._int_to_bool, 'rich_media_provider': str,
			'start_date': self._strpt, 't1as': self._int_to_bool})
		
		
		pass
