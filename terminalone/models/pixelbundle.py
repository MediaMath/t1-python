# -*- coding: utf-8 -*-
"""Provides Pixel Bundle object for working with T1 pixels."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Pixel(Entity):
    """Pixel entity, or entity_type == 'pixel_bundle'"""
    collection = 'pixel_bundles'
    resource = 'pixel_bundle'
    _relations = {
        'advertiser', 'agency', 'provider',
    }
    _roi_fields = t1types.enum({'S1', 'S2', 'V1', 'V2'}, None)
    _pixel_types = t1types.enum({'creative', 'event', 'data', 'segment'},
                                'event')
    _pricing = t1types.enum({'CPM', 'CPTS'}, 'CPM')
    _rmx_conv_types = t1types.enum({'one', 'variable'}, 'one')
    _tag_types = t1types.enum({'dfa', 'uat', 'image', 'iframe', 'js'},
                              'image')
    _pull = {
        'advertiser_id': int,
        'agency_id': int,
        'cost_cpm': float,
        'cost_cpts': float,
        'cost_pct_cpm': float,
        'created_on': t1types.strpt,
        'currency': None,
        'currency_fixed': None,
        'eligible': t1types.int_to_bool,
        'external_identifier': None,
        'id': int,
        'keywords': None,
        'name': None,
        'pixel_type': None,
        'pricing': None,
        'provider_id': int,
        'revenue': None,
        'rmx_conversion_minutes': int,
        'rmx_conversion_type': None,
        'rmx_friendly': t1types.int_to_bool,
        'rmx_merit': t1types.int_to_bool,
        'rmx_pc_window_minutes': int,
        'rmx_pv_window_minutes': int,
        'segment_op': None,
        'status': t1types.int_to_bool,
        'tag_type': None,
        'tags': None,
        'type': None,
        'updated_on': t1types.strpt,
        'version': int,
    }

    _push = _pull.copy()
    _push.update({
        'cost_cpm': t1types.none_to_empty,
        'cost_pct_cpm': t1types.none_to_empty,
        'currency': _roi_fields,
        'eligible': int,
        'pixel_type': _pixel_types,
        'pricing': _pricing,
        'revenue': _roi_fields,
        'rmx_conversion_type': _rmx_conv_types,
        'rmx_friendly': int,
        'rmx_merit': int,
        'status': int,
        'tag_type': _tag_types,
    })
    _readonly = Entity._readonly | {'external_identifier', 'tags', }
    _readonly_update = {'advertiser_id', 'agency_id', 'pixel_type',
                        'provider_id', 'tag_type'}

    def __init__(self, session, properties=None, **kwargs):
        super(Pixel, self).__init__(session, properties, **kwargs)

    def save(self, data=None, url=None):
        """Extra validation for data pixels

        :param data: dict optional data to use instead of self
        :return: None. Object is updated or error is raised
        """
        if self.pixel_type != 'data':
            return super(Pixel, self).save(data=data)

        if data is None:
            data = self._properties.copy()
        if self.pricing == 'CPM':
            data.pop('cost_cpts', None)
            if not getattr(self, 'cost_pct_cpm', None):
                data.pop('cost_pct_cpm', None)
            elif not getattr(self, 'cost_cpm', None):
                data.pop('cost_cpm', None)
        else:
            data.pop('cost_cpm', None)
            data.pop('cost_pct_cpm', None)

        return super(Pixel, self).save(data=data, url=url)


PixelBundle = Pixel
