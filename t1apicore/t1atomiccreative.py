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
		self._readonly.update({'t1as', 'built'})
		self._ad_formats = self._enum({'DISPLAY', 'EXPANDABLE', 'MOBILE'}, 'DISPLAY')
		self._ad_servers = self._enum('ATLAS', 'DART', 'EYEWONDER', 'MEDIAMIND',
									'MEDIAPLEX', 'POINTROLL', 'YIELD_MANAGER',
									'TERMINALONE', 'MEDIAFORGE', 'OTHER'}, 'OTHER')
		self._approved = self._enum({'PENDING', 'APPROVED', 'REJECTED'}, 'PENDING')
		self._expand_dir = self._enum({'L', 'R', 'U', 'D', 'LD', 'RD', 'LU',
											'RU', 'NONRESTRICTED'}, 'NONRESTRICTED')
		self._expand_trig = self._enum({'AUTOMATIC', 'MOUSEOVER', 'CLICK'}, 'CLICK')
		self._file_types = self._enum({'gif', 'jpg', 'swf', 'unknown'}, 'unkown')
		self._tag_types = self._enum({'SCRIPT', 'IFRAME', 'NOSCRIPT'}, 'NOSCRIPT')
		self._pull.update({
			'advertiser_id': int,
			'ad_format': str,
			'ad_server_type': str,
			'approval_status': str,
			'build_errors': str,
			'built': self._int_to_bool,
			'built_by_user_id': int,
			'click_through_url': str,
			'click_url': str,
			'concept_id': int,
			'creative_import_file_id': int,
			'edited_tag': str,
			'end_date': self._strpt,
			'expansion_direction': str,
			'expansion_trigger': str,
			'external_identifier': str,
			'file_type': str,
			'has_sound': self._int_to_bool,
			'height': int,
			'is_https': self._int_to_bool,
			'is_multi_creative': self._int_to_bool,
			'rejected_reason': str,
			'rich_media': self._int_to_bool,
			'rich_media_provider': str,
			'start_date': self._strpt,
			't1as': self._int_to_bool,
			'tag': str,
			'tag_type': str,
			'tpas_ad_tag': str,
			'tpas_ad_tag_name': str,
			'width': int,
		})
		self._push = self._pull.copy()
		self._push.update({
			'ad_format': self._ad_formats,
			'ad_server_type': self._ad_servers,
			'approval_status': self._approved,
			'end_date': self._strft,
			'expansion_direction': self._expand_dir,
			'expansion_trigger': self._expand_trig,
			'file_type': self._file_types,
			'has_sound': int,
			'is_https': int,
			'is_multi_creative': int,
			'rich_media': int,
			'start_date': self._strft,
			't1as': int,
			'tag_type': self._tag_types,
		})
		
		
		pass
# self._types.update({'advertiser_id': int,
# 			'ad_format': str,
# 			'ad_server_type': str,
# 			'approval_status': str,
# 			'build_errors': str,
# 			'built': bool,
# 			'built_by_user_id': int,
# 			'click_through_url': str,
# 			'click_url': str,
# 			'concept_id': int,
# 			'creative_import_file_id': int,
# 			'edited_tag': str,
# 			'end_date': datetime,
# 			'expansion_direction': str,
# 			'expansion_trigger': str,
# 			'external_identifier': str,
# 			'file_type': str,
# 			'has_sound': str,
# 			'height': int,
# 			'is_https': str,
# 			'is_multi_creative': str,
# 			'rejected_reason': str,
# 			'rich_media': bool,
# 			'rich_media_provider': str,
# 			'start_date': datetime,
# 			't1as': bool,
# 			'tag': str,
# 			'tag_type': str,
# 			'tpas_ad_tag': str,
# 			'tpas_ad_tag_name': str,
# 			'width': int,
# 			})
