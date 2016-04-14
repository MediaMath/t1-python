# -*- coding: utf-8 -*-
"""Provides strategy object."""

from __future__ import absolute_import
from functools import partial
import re
from ..config import PATHS
from ..entity import Entity
from ..utils import suppress

PIXEL_PATTERN = re.compile(r'\[(\d+)\]')
OPERATOR_PATTERN = re.compile(r'(AND|OR)')


class Strategy(Entity):
    """Strategy entity."""
    collection = 'strategies'
    resource = 'strategy'
    _relations = {
        'campaign', 'currency', 'time_zone',
    }
    _aud_seg_ops = Entity._enum({'AND', 'OR'}, 'OR')
    _freq_int = Entity._enum({'hour', 'day', 'week', 'month', 'campaign',
                              'not-applicable'}, 'not-applicable')
    _freq_type = Entity._enum({'even', 'asap', 'no-limit'}, 'no-limit')
    _goal_type = Entity._enum({'spend', 'reach', 'cpc', 'cpe', 'cpa', 'roi'},
                              'cpc')
    _media_type = Entity._enum({'DISPLAY', 'VIDEO'}, 'DISPLAY')
    _pac_int = Entity._enum({'hour', 'day'}, 'day')
    _pac_type = Entity._enum({'even', 'asap'}, 'even')
    _site_selec = Entity._enum({'MATHSELECT_250', 'EXCLUDE_UGC', 'ALL',
                                'REDUCED'}, 'REDUCED')
    _supply_type = Entity._enum({'RTB', 'RMX_API', 'T1_RMX'}, 'RTB')
    _type = Entity._enum({'REM', 'GBO', 'AUD'}, 'GBO')

    _pull = {
        'audience_segment_exclude_op': None,
        'audience_segment_include_op': None,
        'bid_aggresiveness': float,
        'bid_price_is_media_only': Entity._int_to_bool,
        'budget': float,
        'campaign_id': int,
        'created_on': Entity._strpt,
        'description': None,
        'effective_goal_value': float,
        'end_date': Entity._strpt,
        'feature_compatibility': None,
        'frequency_amount': int,
        'frequency_interval': None,
        'frequency_type': None,
        'goal_type': None,
        'goal_value': float,
        'id': int,
        'impression_cap': int,
        'max_bid': float,
        'media_type': None,
        'name': None,
        'pacing_amount': float,
        'pacing_interval': None,
        'pacing_type': None,
        'pixel_target_expr': None,
        'roi_target': float,
        'run_on_all_exchanges': Entity._int_to_bool,
        'run_on_all_pmp': Entity._int_to_bool,
        'run_on_display': Entity._int_to_bool,
        'run_on_mobile': Entity._int_to_bool,
        'run_on_streaming': Entity._int_to_bool,
        'site_restriction_transparent_urls': Entity._int_to_bool,
        'site_selectiveness': None,
        'start_date': Entity._strpt,
        'status': Entity._int_to_bool,
        'supply_type': None,
        'type': None,
        'updated_on': Entity._strpt,
        'use_campaign_end': Entity._int_to_bool,
        'use_campaign_start': Entity._int_to_bool,
        'use_mm_freq': Entity._int_to_bool,
        'use_optimization': Entity._int_to_bool,
        'version': int,
        'zone_name': None,
    }
    _push = _pull.copy()
    _push.update({
        'audience_segment_exclude_op': _aud_seg_ops,
        'audience_segment_include_op': _aud_seg_ops,
        'bid_price_is_media_only': int,
        'end_date': partial(Entity._strft, null_on_none=True),
        'frequency_interval': _freq_int,
        'frequency_type': _freq_type,
        'goal_type': _goal_type,
        'media_type': _media_type,
        'pacing_interval': _pac_int,
        'pacing_type': _pac_type,
        'run_on_all_exchanges': int,
        'run_on_all_pmp': int,
        'run_on_display': int,
        'run_on_mobile': int,
        'run_on_streaming': int,
        'site_restriction_transparent_urls': int,
        'site_selectiveness': _site_selec,
        'start_date': partial(Entity._strft, null_on_none=True),
        'status': int,
        'supply_type': _supply_type,
        'type': _type,
        'use_campaign_end': int,
        'use_campaign_start': int,
        'use_mm_freq': int,
        'use_optimization': int,
    })

    _readonly = Entity._readonly | {'effective_goal_value', 'zone_name'}

    def __init__(self, session, properties=None, **kwargs):
        super(Strategy, self).__init__(session, properties, **kwargs)
        try:
            self.pixel_target_expr
        except AttributeError:
            self.pixel_target_expr = ''
        self._deserialize_target_expr()

    def _deserialize_target_expr(self):
        """Deserialize pixel_target_expr string into dict"""
        if 'AND NOT' in self.pixel_target_expr:
            include_string, exclude_string = self.pixel_target_expr.split('AND NOT')
        elif 'NOT' in self.pixel_target_expr:
            include_string, exclude_string = self.pixel_target_expr.split('NOT')
        elif self.pixel_target_expr:
            include_string = self.pixel_target_expr
            exclude_string = ''
        else:
            include_string = ''
            exclude_string = ''
        include_operator = OPERATOR_PATTERN.search(include_string)
        exclude_operator = OPERATOR_PATTERN.search(exclude_string)
        if include_operator:
            include_operator = include_operator.group(0)
        if exclude_operator:
            exclude_operator = exclude_operator.group(0)
        self.pixel_target_expr = {
            'include': {
                'pixels': [int(pix) for pix in PIXEL_PATTERN.findall(include_string)],
                'operator': include_operator,
            },
            'exclude': {
                'pixels': [int(pix) for pix in PIXEL_PATTERN.findall(exclude_string)],
                'operator': exclude_operator,
            },
        }

    def save_supplies(self, data):
        url = self._construct_url(addl=['supplies', ])
        entity, _ = super(Strategy, self)._post(PATHS['mgmt'], url, data)
        self._update_self(next(entity))
        self._deserialize_target_expr()
        if 'relations' in self.properties:
            del self.properties['relations']

    def save_domains(self, data):
        url = self._construct_url(addl=['domain_restrictions', ])
        # this endpoint doesn't return an entity like the supplies endpoint
        # so we ignore the error
        with suppress(AttributeError):
            entity, _ = super(Strategy, self)._post(PATHS['mgmt'], url, data)

            # you can't get these values so we don't need to reset anything

    def save_audience_segments(self, data):
        url = self._construct_url(addl=['audience_segments', ])
        entity, _ = super(Strategy, self)._post(PATHS['mgmt'], url, data)

    def _serialize_target_expr(self):
        """Serialize pixel_target_expr dict into string"""
        include_bool = '] {} ['.format(self.pixel_target_expr['include']['operator'] or 'OR')
        include_pixels = self.pixel_target_expr['include']['pixels']
        exclude_bool = '] {} ['.format(self.pixel_target_expr['exclude']['operator'] or 'OR')
        exclude_pixels = self.pixel_target_expr['exclude']['pixels']
        include_string = '( [{}] )'.format(include_bool.join(
            str(pix) for pix in include_pixels)) if include_pixels else ''
        exclude_string = 'NOT ( [{}] )'.format(exclude_bool.join(
            str(pix) for pix in exclude_pixels)) if exclude_pixels else ''
        if include_string and exclude_string:
            return '{} AND {}'.format(include_string, exclude_string)
        else:
            return include_string + exclude_string

    def save(self, data=None, url=None):

        if data is None:
            data = self.properties.copy()

        data['pixel_target_expr'] = self._serialize_target_expr()

        if getattr(self, 'use_campaign_start', False) and 'start_date' in data:
            self.properties.pop('start_date', None)
            data['start_date'] = None
        if getattr(self, 'use_campaign_end', False) and 'end_date' in data:
            self.properties.pop('end_date', None)
            data['end_date'] = None

        super(Strategy, self).save(data=data, url=url)

        self._deserialize_target_expr()

    @property
    def pixel_target_expr_string(self):
        """Return string version of pixel_target_expr"""
        return self._serialize_target_expr()
