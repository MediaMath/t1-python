# -*- coding: utf-8 -*-
"""Provides strategy object."""

from __future__ import absolute_import
from functools import partial
import re
from .. import t1types
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
    _seg_incexc_ops = t1types.enum({'AND', 'OR'}, 'OR')
    _pacing_ints = t1types.enum({'hour', 'day', 'week', 'month', 'campaign',
                                'not-applicable'}, 'not-applicable')
    _pacing_types = t1types.enum({'even', 'asap', 'no-limit'}, 'no-limit')
    _goal_type = t1types.enum({'spend', 'reach', 'cpc', 'cpe', 'cpa', 'roi'},
                              'cpc')
    _media_type = t1types.enum({'DISPLAY', 'VIDEO'}, 'DISPLAY')
    _pac_int = t1types.enum({'hour', 'day'}, 'day')
    _pac_type = t1types.enum({'even', 'asap'}, 'even')
    _site_selec = t1types.enum({'MATHSELECT_250', 'EXCLUDE_UGC', 'ALL',
                                'REDUCED'}, 'REDUCED')
    _supply_types = t1types.enum({'RTB', 'RMX_API', 'T1_RMX', 'MKT', 'BATCH'},
                                 'RTB')
    _type = t1types.enum({'REM', 'GBO', 'AUD'}, 'GBO')

    _pull = {
        'audience_segment_exclude_op': None,
        'audience_segment_include_op': None,
        'bid_aggressiveness': float,
        'bid_price_is_media_only': t1types.int_to_bool,
        'budget': float,
        'campaign_id': int,
        'created_on': t1types.strpt,
        'currency_code': None,
        'description': None,
        'effective_goal_value': float,
        'end_date': t1types.strpt,
        'feature_compatibility': None,
        'frequency_amount': int,
        'frequency_interval': None,
        'frequency_optimization': t1types.int_to_bool,
        'frequency_type': None,
        'goal_type': None,
        'goal_value': float,
        'id': int,
        'impression_cap': int,
        'impression_pacing_amount': int,
        'impression_pacing_interval': None,
        'impression_pacing_type': None,
        'max_bid': float,
        'max_bid_wm': float,
        'media_type': None,
        'name': None,
        'pacing_amount': float,
        'pacing_interval': None,
        'pacing_type': None,
        'pixel_target_expr': None,
        'roi_target': float,
        'run_on_all_exchanges': t1types.int_to_bool,
        'run_on_all_pmp': t1types.int_to_bool,
        'run_on_display': t1types.int_to_bool,
        'run_on_mobile': t1types.int_to_bool,
        'run_on_streaming': t1types.int_to_bool,
        'site_restriction_transparent_urls': t1types.int_to_bool,
        'site_selectiveness': None,
        'start_date': t1types.strpt,
        'status': t1types.int_to_bool,
        'supply_type': None,
        'targeting_segment_exclude_op': None,
        'targeting_segment_include_op': None,
        'type': None,
        'updated_on': t1types.strpt,
        'use_campaign_end': t1types.int_to_bool,
        'use_campaign_start': t1types.int_to_bool,
        'use_mm_freq': t1types.int_to_bool,
        'use_optimization': t1types.int_to_bool,
        'version': int,
        'zone_name': None,
    }
    _push = _pull.copy()
    _push.update({
        'audience_segment_exclude_op': _seg_incexc_ops,
        'audience_segment_include_op': _seg_incexc_ops,
        'bid_price_is_media_only': int,
        'end_date': partial(t1types.strft, null_on_none=True),
        'frequency_interval': _pacing_ints,
        'frequency_optimization': int,
        'frequency_type': _pacing_types,
        'goal_type': _goal_type,
        'impression_pacing_interval': _pacing_ints,
        'impression_pacing_type': _pacing_types,
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
        'start_date': partial(t1types.strft, null_on_none=True),
        'status': int,
        'supply_type': _supply_types,
        'targeting_segment_exclude_op': _seg_incexc_ops,
        'targeting_segment_include_op': _seg_incexc_ops,
        'type': _type,
        'use_campaign_end': int,
        'use_campaign_start': int,
        'use_mm_freq': int,
        'use_optimization': int,
    })

    _readonly = Entity._readonly | {'effective_goal_value', 'zone_name'}

    def __init__(self, session, properties=None, **kwargs):
        super(Strategy, self).__init__(session, properties, **kwargs)

        if properties is None:
            # super(Entity) supers to grandparent
            super(Entity, self).__setattr__('_init_impcap', None)
            super(Entity, self).__setattr__('_init_imppac', None)
        else:
            super(Entity, self).__setattr__('_init_impcap',
                                            properties.get('impression_cap'))
            super(Entity, self).__setattr__('_init_imppac',
                                            (properties.get('impression_pacing_type'),
                                             properties.get('impression_pacing_amount'),
                                             properties.get('impression_pacing_interval')))

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

    def _migration_asst(self):
        """Helps migrate users to the new impression pacing features.

        impression_cap is the old field. impression pacing comprise the new.
        If the user has changed:
            - Nothing (final vals all equal): remove both fields
            - Old (new vals equal): remove new fields, post old
            - New (old vals equal): remove old fields, post new
            - Both (no vals equal): UNDEFINED. remove old fields to prep.
        """
        new_fields = ['impression_pacing_type',
                      'impression_pacing_amount',
                      'impression_pacing_interval']
        i_cap, i_pac = self._init_impcap, self._init_imppac
        f_cap, f_pac = (self.properties.get('impression_cap'),
                        (self.properties.get('impression_pacing_type'),
                         self.properties.get('impression_pacing_amount'),
                         self.properties.get('impression_pacing_interval')))

        fields_to_remove = None
        if i_cap == f_cap and i_pac == f_pac:
            fields_to_remove = ['impression_cap']
            fields_to_remove.extend(new_fields)
        elif i_pac == f_pac:
            fields_to_remove = new_fields
        else:  # we don't need a second elif here because it's the same result
            fields_to_remove = ['impression_cap']
        return fields_to_remove

    def save_supplies(self, data):
        url = self._construct_url(addl=['supplies', ])
        entity, _ = super(Strategy, self)._post(PATHS['mgmt'], url, data)
        self._update_self(entity)
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

    def save_targeting_segments(self, data):
        url = self._construct_url(addl=['targeting_segments', ])
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
        """Save object to T1 accounting for fields an pixel target expr"""
        if data is None:
            data = self.properties.copy()

        data['pixel_target_expr'] = self._serialize_target_expr()

        fields_to_remove = self._migration_asst()
        for field in fields_to_remove:
            data.pop(field, None)

        if getattr(self, 'use_campaign_start', False) and 'start_date' in data:
            self.properties.pop('start_date', None)
            data['start_date'] = None
        if getattr(self, 'use_campaign_end', False) and 'end_date' in data:
            self.properties.pop('end_date', None)
            data['end_date'] = None

        super(Strategy, self).save(data=data, url=url)

        # Re-set the fields so that if the same object get saved, we
        # compare agains the re-initialized values
        self._deserialize_target_expr()
        super(Entity, self).__setattr__('_init_impcap',
                                        self.properties.get('impression_cap'))
        super(Entity, self).__setattr__('_init_imppac',
                                        (self.properties.get('impression_pacing_type'),
                                         self.properties.get('impression_pacing_amount'),
                                         self.properties.get('impression_pacing_interval')))

    @property
    def pixel_target_expr_string(self):
        """Return string version of pixel_target_expr"""
        return self._serialize_target_expr()
