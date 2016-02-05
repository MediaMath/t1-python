# -*- coding: utf-8 -*-
"""Provides Atomic Creative object for working with creatives."""

from __future__ import absolute_import
from ..entity import Entity


class AtomicCreative(Entity):
    """T1 Creative entity, or an atomic_creative entity."""
    collection = 'atomic_creatives'
    resource = 'atomic_creative'
    _relations = {
        'advertiser', 'concept', 'creative_approvals', 'creatives',
    }
    _ad_formats = Entity._enum({'DISPLAY', 'EXPANDABLE', 'MOBILE'},
                               'DISPLAY')
    _ad_servers = Entity._enum({'ATLAS', 'DART', 'EYEWONDER', 'MEDIAMIND',
                                'MEDIAPLEX', 'POINTROLL', 'YIELD_MANAGER',
                                'TERMINALONE', 'MEDIAFORGE', 'OTHER'},
                               'OTHER')
    _expands = Entity._enum({'L', 'R', 'U', 'D', 'LD', 'RD', 'LU', 'RU'}, None)
    _expand_dir = Entity._default_empty('NONRESTRICTED')
    _expand_trig = Entity._enum({'AUTOMATIC', 'MOUSEOVER', 'CLICK'}, 'CLICK')
    _file_types = Entity._enum({'swf', 'gif', 'html5', 'jpg', 'jpeg', 'tif',
                                'tiff', 'png', 'unknown', 'vast'}, 'unknown')
    _media_types = Entity._enum({'display', 'video', 'mobile'}, 'display')
    _tag_types = Entity._enum({'IFRAME_SCRIPT_NOSCRIPT', 'IFRAME_SCRIPT',
                               'IFRAME_NOSCRIPT', 'IFRAME_IMG',
                               'SCRIPT_NOSCRIPT', 'SCRIPT', 'NOSCRIPT',
                               'IFRAME', 'IMG'}, 'NOSCRIPT')
    _pull = {
        'advertiser_id': int,
        'ad_format': None,
        'ad_server_type': None,
        'approval_status': None,
        'build_date': Entity._strpt,
        'build_errors': None,
        'built': Entity._int_to_bool,
        'built_by_user_id': int,
        'click_through_url': None,
        'click_url': None,
        'concept_id': int,
        'created_on': Entity._strpt,
        'creative_import_file_id': int,
        'edited_tag': None,
        'end_date': Entity._strpt,
        'expand': None,
        'expansion_direction': None,
        'expansion_trigger': None,
        'external_identifier': None,
        'file_type': None,
        'has_sound': Entity._int_to_bool,
        'height': int,
        'id': int,
        'is_https': Entity._int_to_bool,
        'is_multi_creative': Entity._int_to_bool,
        'last_modified': Entity._strpt,
        'media_type': None,
        'name': None,
        'rejected_reason': None,
        'rich_media': Entity._int_to_bool,
        'rich_media_provider': None,
        'start_date': Entity._strpt,
        'status': Entity._int_to_bool,
        't1as': Entity._int_to_bool,
        'tag': None,
        'tag_type': None,
        'tpas_ad_tag': None,
        'tpas_ad_tag_name': None,
        'type': None,
        'updated_on': Entity._strpt,
        'version': int,
        'width': int,
    }
    _push = _pull.copy()
    _push.update({
        'ad_format': _ad_formats,
        'ad_server_type': _ad_servers,
        'end_date': Entity._strft,
        'expand': _expands,
        'expansion_direction': _expand_dir,
        'expansion_trigger': _expand_trig,
        'file_type': _file_types,
        'has_sound': int,
        'is_https': int,
        'is_multi_creative': int,
        'media_type': _media_types,
        'rich_media': int,
        'start_date': Entity._strft,
        'status': int,
        't1as': int,
        'tag_type': _tag_types,
    })
    _readonly = Entity._readonly | {'t1as', 'built', 'approval_status',
                                    'default_t1as_tag', 'rejected_reason'}

    def __init__(self, session, properties=None, **kwargs):
        super(AtomicCreative, self).__init__(session, properties, **kwargs)
