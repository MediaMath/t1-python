# -*- coding: utf-8 -*-
"""Provides base object for T1 data classes."""

from __future__ import absolute_import, division
from datetime import datetime, timedelta
from warnings import warn
from .config import PATHS
from .connection import Connection
from .errors import ClientError
from terminalone.utils import FixedOffset
from .vendor import six


class Entity(Connection):
    """Superclass for all the various T1 entities.

    Implements methods for data validation and saving to T1. Entity and its
    subclasses should not be instantiated directly; instead, an instance of
    T1 should instantiate these classes, passing in the proper session, etc.
    """
    _readonly = {'id', 'build_date', 'created_on',
                 '_type',  # _type is used because "type" is taken by User.
                 'updated_on', 'last_modified'}
    _readonly_update = set()

    def __init__(self, session, properties=None, **kwargs):
        """Passes session to underlying connection and validates properties passed in.

        Entity, or any class deriving from it, should never be instantiated directly.
        `T1` class should, with session information, instantiate the relevant
        subclass.
        :param session: requests.Session to be used
        :param properties: dict of entity properties
        :param kwargs: additional kwargs to pass to Connection
        """

        # __setattr__ is overridden below. So, to set self.properties as an empty
        # dict, we need to use the built-in __setattr__ method; thus, super()
        super(Entity, self).__init__(_create_session=False, **kwargs)
        super(Entity, self).__setattr__('session', session)
        if properties is None:
            super(Entity, self).__setattr__('properties', {})
            return

        for attr, val in six.iteritems(properties):
            if self._pull.get(attr) is not None:
                properties[attr] = self._pull[attr](val)
        super(Entity, self).__setattr__('properties', properties)

    def __repr__(self):
        return '{cname}({props})'.format(
            cname=type(self).__name__,
            props=', '.join(
                '{key}={value!r}'.format(key=key, value=value)
                for key, value in six.iteritems(self.properties)
            )
        )

    def __getitem__(self, attribute):
        """DEPRECATED way of retrieving properties like with dictionary"""
        warn('Accessing entity like a dictionary will be removed: '
             'please discontinue use.',
             DeprecationWarning, stacklevel=2)
        if attribute in self.properties:
            return self.properties[attribute]
        else:
            raise AttributeError(attribute)

    def __setitem__(self, attribute, value):
        """DEPRECATED way of setting properties like with dictionary"""
        warn('Accessing entity like a dictionary will be removed: '
             'please discontinue use.',
             DeprecationWarning, stacklevel=2)
        self.properties[attribute] = self._pull[attribute](value)

    def __getattr__(self, attribute):
        if attribute in self.properties:
            return self.properties[attribute]
        else:
            raise AttributeError(attribute)

    def __setattr__(self, attribute, value):
        if self._pull.get(attribute) is not None:
            self.properties[attribute] = self._pull[attribute](value)
        else:
            self.properties[attribute] = value

    def __delattr__(self, attribute):
        if attribute in self.properties:
            del self.properties[attribute]
        else:
            raise AttributeError(attribute)

    def __getstate__(self):
        """Custom pickling. TODO"""
        return super(Entity, self).__getstate__()

    def __setstate__(self, state):
        """Custom unpickling. TODO"""
        return super(Entity, self).__setstate__(state)

    @staticmethod
    def _int_to_bool(value):
        """Convert integer string {"0","1"} to its corresponding bool"""
        return bool(int(value))

    @staticmethod
    def _none_to_empty(val):
        """Convert None to empty string.

        Necessary for fields that are required POST but have no logical value.
        """
        if val is None:
            return ""
        return val

    @staticmethod
    def _enum(all_vars, default):
        """Check input against accepted set or return a default."""

        def get_value(test_value):
            if test_value in all_vars:
                return test_value
            else:
                return default

        return get_value

    @staticmethod
    def _default_empty(default):
        """Check an input against its falsy value or return a default."""

        def get_value(test_value):
            if test_value:
                return test_value
            else:
                return default

        return get_value

    @staticmethod
    def _strpt(dt_string):
        """Convert ISO string time to datetime.datetime. No-op on datetimes"""
        if isinstance(dt_string, datetime):
            return dt_string
        if dt_string[-5] == '-' or dt_string[-5] == '+':
            offset_str = dt_string[-5:]
            dt_string = dt_string[:-5]
            offset = int(offset_str[-4:-2]) * 60 + int(offset_str[-2:])
            if offset_str[0] == "-":
                offset = -offset
        else:
            offset = 0

        return datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=FixedOffset(offset))

    @staticmethod
    def _strft(dt_obj, null_on_none=False):
        """Convert datetime.datetime to ISO string.

        :param null_on_none: bool Occasionally, we will actually want to send an
            empty string where a datetime would typically go. For instance, if a
            strategy has an end_date set, but then wants to change to use
            campaign end date, the POST will normally omit the end_date field
            (because you cannot send it with use_campaign_end).
            However, this will cause an error because there was an end_date set
            previously. So, we need to send an empty string to indicate that it
            should be nulled out. In cases like this, null_on_none should be set
            to True in the entity's _push dict using a partial to make it a
            single-argument function. See strategy.py
        :raise AttributeError: if not provided a datetime
        :return: str
        """
        try:
            return dt_obj.strftime("%Y-%m-%dT%H:%M:%S")
        except AttributeError:
            if dt_obj is None and null_on_none:
                return ""
            raise

    def _validate_read(self, data):
        """Convert XML strings to Python objects"""
        for key, value in six.iteritems(data):
            if key in self._pull:
                data[key] = self._pull[key](value)
        return data

    def _conds_for_removal(self, key, update, push_fn):
        """Determine if an attribute should be removed before POST.

        Attributes should be removed if we don't expect them or if they
        aren't to be written to. Because relations are incliuded as attributes
        as well, remove these too.
        """
        return (key in self._readonly or
                key in self._relations or
                (update and key in self._readonly_update) or
                push_fn is False)

    def _validate_write(self, data):
        """Convert Python objects to XML values.

        If attribute should not be sent, remove it from the body.
        """
        update = 'id' in self.properties
        if 'version' not in data and update:
            data['version'] = self.version
        for key, value in six.iteritems(data.copy()):
            push_fn = self._push.get(key, False)

            if self._conds_for_removal(key, update, push_fn):
                del data[key]
                continue

            if push_fn is not None:
                data[key] = self._push[key](value)
            else:
                data[key] = value
        return data

    def _construct_url(self, addl=None):
        """Construct URL for post.

        Collection, ID if present, additional values (like "history") if needed.
        """
        url = [self.collection, ]

        if self.properties.get('id'):
            url.append(str(self.id))
        if addl is not None:
            url.extend(addl)

        return '/'.join(url)

    def _update_self(self, entity):
        """Update own properties based on values returned by API."""
        for key, value in six.iteritems(entity):
            setattr(self, key, value)

    def is_property(self, prop):
        if prop in self._pull:
            return True
        return False

    def set(self, properties):
        """Set properties for object from given dict of properties.

        Essentially a merge.
        """
        for attr, value in six.iteritems(properties):
            setattr(self, attr, value)

    def save(self, data=None, url=None):
        """Save object to T1."""
        if url is None:
            url = self._construct_url()
        if data is not None:
            data = self._validate_write(data)
        else:
            data = self._validate_write(self.properties)
        entity, _ = super(Entity, self)._post(PATHS['mgmt'], url, data=data)
        self._update_self(next(entity))

    def update(self, *args, **kwargs):
        """Alias for save"""
        return self.save(*args, **kwargs)

    def history(self):
        """Retrieve changelog entry for entity."""
        if not self.properties.get('id'):
            raise ClientError('Entity ID not given')
        url = self._construct_url(addl=['history', ])
        history, _ = super(Entity, self)._get(PATHS['mgmt'], url)
        return history


class SubEntity(Entity):
    """Sub-entity, denoted by object like /collection/:id/sub-entity.

    These objects need URLs constructed differently.
    """

    def _construct_url(self, addl=None):
        url = [self.parent, str(self.parent_id), self.collection]

        if self.properties.get('id'):
            url.append(str(self.id))
        if addl is not None:
            url.extend(addl)
        return '/'.join(url)
