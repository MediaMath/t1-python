# -*- coding: utf-8 -*-
"""Provides contact object."""

from __future__ import absolute_import
from .. import t1types
from ..entity import Entity


class Contact(Entity):
    """Concept entity."""
    collection = 'contacts'
    resource = 'contact'
    _pull = {
        'id': int,
        'version': int,
        'first_name': None,
        'last_name': None,
        'title': None,
        'phone': None,
        'mobile': None,
        'fax': None,
        'email': None,
        'address_1': None,
        'address_2': None,
        'city': None,
        'state': None,
        'zip': None,
        'country': None,
        'created_on': t1types.strpt,
        'updated_on': t1types.strpt,
    }
    _push = _pull.copy()

    def __init__(self, session, properties=None, **kwargs):
        super(Contact, self).__init__(session, properties, **kwargs)
