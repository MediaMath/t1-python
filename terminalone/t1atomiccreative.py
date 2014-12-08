# -*- coding: utf-8 -*-
"""Provides Atomic Creative object for working with creatives.

Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from .t1object import T1Object
# IMPORT

class T1AtomicCreative(T1Object):
	"""docstring for T1AtomicCreative"""
	collection = 'atomic_creatives'
	type = 'atomic_creative'
	_relations = {
		'advertiser', 'concept', 'creatives',
	}
	_ad_formats = T1Object._enum({'DISPLAY', 'EXPANDABLE', 'MOBILE'},
									'DISPLAY')
	_ad_servers = T1Object._enum({'ATLAS', 'DART', 'EYEWONDER', 'MEDIAMIND',
								'MEDIAPLEX', 'POINTROLL', 'YIELD_MANAGER',
								'TERMINALONE', 'MEDIAFORGE', 'OTHER'}, 'OTHER')
	_approved = T1Object._enum({'PENDING', 'APPROVED', 'REJECTED'}, 'PENDING')
	_expand_dir = T1Object._enum({'L', 'R', 'U', 'D', 'LD', 'RD', 'LU',
									'RU', 'NONRESTRICTED'}, 'NONRESTRICTED')
	_expand_trig = T1Object._enum({'AUTOMATIC', 'MOUSEOVER', 'CLICK'},'CLICK')
	_file_types = T1Object._enum({'gif', 'jpg', 'swf', 'unknown'}, 'unknown')
	_tag_types = T1Object._enum({'SCRIPT', 'IFRAME', 'NOSCRIPT'}, 'NOSCRIPT')
	_pull = {
		'advertiser_id': int,
		'ad_format': None,
		'ad_server_type': None,
		'approval_status': None,
		'build_date': T1Object._strpt,
		'build_errors': None,
		'built': T1Object._int_to_bool,
		'built_by_user_id': int,
		'click_through_url': None,
		'click_url': None,
		'concept_id': int,
		'created_on': T1Object._strpt,
		'creative_import_file_id': int,
		'edited_tag': None,
		'end_date': T1Object._strpt,
		'expansion_direction': None,
		'expansion_trigger': None,
		'external_identifier': None,
		'file_type': None,
		'has_sound': T1Object._int_to_bool,
		'height': int,
		'id': int,
		'is_https': T1Object._int_to_bool,
		'is_multi_creative': T1Object._int_to_bool,
		'last_modified': T1Object._strpt,
		'name': None,
		'rejected_reason': None,
		'rich_media': T1Object._int_to_bool,
		'rich_media_provider': None,
		'start_date': T1Object._strpt,
		'status': T1Object._int_to_bool,
		't1as': T1Object._int_to_bool,
		'tag': None,
		'tag_type': None,
		'tpas_ad_tag': None,
		'tpas_ad_tag_name': None,
		'type': None,
		'updated_on': T1Object._strpt,
		'version': int,
		'width': int,
	}
	_push = _pull.copy()
	_push.update({
		'ad_format': _ad_formats,
		'ad_server_type': _ad_servers,
		# 'approval_status': _approved,
		'end_date': T1Object._strft,
		'expansion_direction': _expand_dir,
		'expansion_trigger': _expand_trig,
		'file_type': _file_types,
		'has_sound': int,
		'is_https': int,
		'is_multi_creative': int,
		'rich_media': int,
		'start_date': T1Object._strft,
		'status': int,
		't1as': int,
		'tag_type': _tag_types,
	})
	_readonly = T1Object._readonly.copy()
	_readonly.update({'t1as', 'built, approval_status'})
	def __init__(self, session, properties=None, **kwargs):
		super(T1AtomicCreative, self).__init__(session, properties, **kwargs)
