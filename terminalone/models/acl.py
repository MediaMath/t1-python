# -*- coding: utf-8 -*-
"""Provides acl object."""

from __future__ import absolute_import
from ..errors import ClientError
from ..entity import SubEntity
from ..vendor import six


class ACL(SubEntity):
    """docstring for ACL."""
    collection = 'acl'
    resource = 'acl'
    _pull = {
        '_type': None,
        'editable': None,
    }

    def __init__(self, session, properties=None, **kwargs):
        for key in six.iterkeys(properties):
            if '_id' in key:
                self._pull[key] = int
        super(ACL, self).__init__(session, properties, **kwargs)

    def save(self, *args, **kwargs):
        raise ClientError('This object is not editable.')
