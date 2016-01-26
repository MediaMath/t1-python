# -*- coding: utf-8 -*-
"""Provides margin object."""

from __future__ import absolute_import
from ..errors import ClientError
from ..entity import SubEntity
from ..vendor import six

class Margin(SubEntity):
    """docstring for Margin."""
    collection = 'margins'
    resource = 'margins'

    _pull = {
        '_type': None,
        'margin_date': None,
        'campaign_id': None,
        'margin_pct': None,
    }

    def __init__(self, session, properties=None, **kwargs):
        super(Margin, self).__init__(session, properties, **kwargs)