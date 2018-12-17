# -*- coding: utf-8 -*-
"""Provides base object for T1 data classes."""

from __future__ import absolute_import, division
from terminalone import t1types
from .connection import Connection
from .errors import ClientError
from .vendor import six


class Entity(Connection):
    """Superclass for all the various T1 entities.

    Implements methods for data validation and saving to T1. Entity and its
    subclasses should not be instantiated directly; instead, an instance of
    T1 should instantiate these classes, passing in the proper session, etc.
    """

    _post_format = 'formdata'
    _relations = {}
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

        # __setattr__ is overridden below. So to set self._properties as an empty
        # dict, we need to use the built-in __setattr__ method
        super(Entity, self).__init__(_create_session=False, **kwargs)
        super(Entity, self).__setattr__('session', session)

        if properties is None:
            properties = {}
        super(Entity, self).__setattr__('is_update', 'id' in properties)
        self._update_self(properties)

    def __repr__(self):
        properties = self.get_properties()
        return '{cname}({props})'.format(
            cname=type(self).__name__,
            props=', '.join(
                '{key}={value!r}'.format(key=key, value=value)
                for key, value in six.iteritems(properties)
            )
        )

    def __getattr__(self, attribute):
        if attribute in self._properties:
            return self._properties[attribute]
        elif attribute in self._init_properties:
            return self._init_properties[attribute]
        else:
            raise AttributeError(attribute)

    def __setattr__(self, attribute, value):
        if value is not None and self._pull.get(attribute) is not None:
            try:
                self._properties[attribute] = self._pull[attribute](value)
            except ValueError:
                raise ClientError('key {} is invalid: must be of type {}'
                                  .format(attribute, self._pull[attribute]))
            except TypeError as e:
                raise ClientError('key {} is invalid: {}'
                                  .format(attribute, e.message))
        else:
            self._properties[attribute] = value

    def __delattr__(self, attribute):
        if attribute in self._init_properties:
            self._properties[attribute] = t1types.Deleted(self._init_properties[attribute])
        else:
            raise AttributeError(attribute)

    def _conds_for_removal(self, key, push_fn):
        """Determine if an attribute should be removed before POST.

        Attributes should be removed if we don't expect them or if they
        aren't to be written to. Because relations are incliuded as attributes
        as well, remove these too.
        """
        return (key in self._readonly or
                key in self._relations or
                (self.is_update and key in self._readonly_update) or
                push_fn is False)

    def _validate_json_post(self, data):
        """Convert Python objects to POST values.

        If attribute should not be sent, remove it from the body.
        """
        for key, value in six.iteritems(data.copy()):
            push_fn = self._push.get(key, False)

            if value is None or self._conds_for_removal(key, push_fn):
                del data[key]
                continue

            if push_fn and value is not None:
                try:
                    data[key] = self._push[key](value)
                except ValueError:
                    raise ClientError('key {} is invalid: must be of type {}'
                                      .format(key, self._push[key]))
                except TypeError as e:
                    raise ClientError('key {} is invalid: {}'
                                      .format(key, e.message))
            else:
                data[key] = value
        return data

    def _validate_form_post(self, data):
        """Convert Python objects to POST values.

        If attribute should not be sent, remove it from the body.
        """
        if 'version' not in data and self.is_update:
            data['version'] = self.version

        for key, value in six.iteritems(data.copy()):
            push_fn = self._push.get(key, False)

            if self._conds_for_removal(key, push_fn):
                del data[key]
                continue

            if isinstance(value, t1types.Deleted):
                data[key] = value.get_value()
            else:
                if push_fn:
                    try:
                        data[key] = self._push[key](value)
                    except ValueError:
                        raise ClientError('key {} is invalid: must be of type {}'
                                          .format(key, self._push[key]))
                    except TypeError as e:
                        raise ClientError('key {} is invalid: {}'
                                          .format(key, e.message))
                else:
                    data[key] = value
        return data

    def _construct_url(self, addl=None):
        """Construct URL for post.

        Collection, ID if present, additional values (like "history") if needed.
        """
        url = [self.collection, ]

        if self._init_properties.get('id'):
            url.append(str(self.id))
        if addl is not None:
            url.extend(addl)

        return '/'.join(url)

    def _update_self(self, properties):
        """Update own properties based on values returned by API."""
        for attr, val in six.iteritems(properties):
            if self._pull.get(attr) is not None and val is not None:
                properties[attr] = self._pull[attr](val)
        super(Entity, self).__setattr__('_init_properties', properties)
        self._reset_properties(properties)

    def get_properties(self):
        properties = {}
        properties.update(self._init_properties)
        properties.update(self._properties)
        return properties

    def _reset_properties(self, properties):
        super(Entity, self).__setattr__('_init_properties', properties)
        if self.is_update:
            super(Entity, self).__setattr__('_properties', {})
        else:
            super(Entity, self).__setattr__('_properties', properties)

    def revert(self):
        super(Entity, self).__setattr__('_properties', {})

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
        if data is None:
            data = self._properties

        if self._post_format is 'formdata':
            data = self._validate_form_post(data)
            entity, _ = super(Entity, self)._post(self._get_service_path(), url, data=data)
        else:
            data = self._validate_json_post(data)
            entity, _ = super(Entity, self)._post(self._get_service_path(), url, json=data)

        self._update_self(entity)

    def get_formdata(self, data=None, includeunchanged=False):
        if data is None:
            data = self._properties.copy()
        if includeunchanged:
            data = self._init_properties.copy()
            data.update(self._properties)
        return self._validate_form_post(data)

    def update(self, *args, **kwargs):
        """Alias for save"""
        return self.save(*args, **kwargs)

    def history(self):
        """Retrieve changelog entry for entity."""
        if not self._init_properties.get('id'):
            raise ClientError('Entity ID not given')
        url = self._construct_url(addl=['history', ])
        history, _ = super(Entity, self)._get(self._get_service_path(), url)
        return history


class SubEntity(Entity):
    """Sub-entity, denoted by object like /collection/:id/sub-entity.

    These objects need URLs constructed differently.
    """

    def _construct_url(self, addl=None):
        url = [self.parent, str(self.parent_id), self.collection]

        if self._init_properties.get('id'):
            url.append(str(self.id))
        if addl is not None:
            url.extend(addl)
        return '/'.join(url)
