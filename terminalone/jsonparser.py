# -*- coding: utf-8 -*-
"""Parses JSON output from T1 and returns a Python object"""

from __future__ import absolute_import
import json
try:
    from itertools import imap
    map = imap
except ImportError:
    pass
from .errors import (T1Error, ValidationError, ParserException, STATUS_CODES)
from terminalone.vendor import six


class FindKey:
    def __init__(self, data, key):
        self.i = 0
        self.json = data
        self.key = key

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.json = self.json[self.key]
            return self.json
        except KeyError:
            raise StopIteration()

    def next(self):
        return self.__next__()


class JSONParser(object):
    """Parses JSON response"""

    def __init__(self, body):
        self.status_code = False
        try:
            parsed_data = json.loads(body)
        except ValueError as e:
            raise ParserException(e)

        self.get_status(parsed_data, body)

        try:
            self.entity_count = int(parsed_data['meta']['total_count'])
        except KeyError:
            self.entity_count = 1

        data = parsed_data.get('data')

        if type(data) == list:
            self.entities = map(self.process_entity, data)

        elif data.get('include') is not None or \
                data.get('exclude') is not None or \
                data.get('enabled') is not None:
            self.entities = self._parse_target_dimensions(data)

        # FIXME: permissions responses dont have an 'entity_type' field so we're using the
        # FIXME: absence of this field to identify whether it's a permissions object
        # FIXME: or just a field named 'permissions'. As always, negative tests are bad. baaaaad.
        elif data.get('permissions') is not None and data.get('entity_type') is None:
            self.entities = self._parse_permissions(data['permissions'])

        else:
            self.entities = next(map(self.process_entity,
                                     FindKey(parsed_data, 'data')))

    def get_status(self, data, body):
        """Gets the status code of T1 JSON.

        If code is valid, returns None; otherwise raises the appropriate Error.
        """
        try:
            status_code = data['meta']['status']
        except KeyError:
            raise T1Error(None, body)

        try:
            exc = STATUS_CODES[status_code]
        except KeyError:
            self.status_code = False
            raise T1Error(status_code, status_code)

        if exc is None:
            self.status_code = True
            return

        if exc is True:
            message = self._parse_field_error(data)
            exc = ValidationError
        else:
            message = self._parse_error_messages(data)

        raise exc(code=status_code, content=message, body=data)

    def _parse_permissions(self, permissions):
        """Iterate over permissions and parse into dicts"""
        entity_root = permissions.get('entities')
        organization, agency, advertiser = None, None, None
        if entity_root:
            advertiser = self.process_permission(entity_root.get('advertiser'), 'advertiser')
            agency = self.process_permission(entity_root.get('agency'), 'agency')
            organization = self.process_permission(entity_root.get('organization'), 'organization')

        flags = self.process_permission(permissions.get('flags'), 'flags')
        flags.update({
            '_type': 'permission',
            'advertiser': advertiser,
            'agency': agency,
            'organization': organization,
        })

        return flags

    def _parse_target_dimensions(self, data):
        """Iterate over target dimensions and parse into dicts"""
        exclude_entities = data.get('exclude')
        include_entities = data.get('include')
        if include_entities is not None:
            include_list = map(self.process_entity, include_entities)
        else:
            include_list = []
        if exclude_entities is not None:
            exclude_list = map(self.process_entity, exclude_entities)
        else:
            exclude_list = []
        self.entity_count = 1
        return {
            '_type': 'target_dimension',
            'exclude': exclude_list,
            'include': include_list,
        }

    @staticmethod
    def _parse_error_messages(data):
        """Iterate over field errors and parse into dicts"""
        errors = []
        for error in data['errors']:
            errors.append(error['message'])
        return ', '.join(errors)

    @staticmethod
    def _parse_field_error(data):
        """Iterate over field errors and parse into dicts"""
        errors = {}
        for error in data['errors']:
            if error.get('field') is None:
                pass
            else:
                errors[error['field']] = {
                    'error': error['message']}
        return errors

    @classmethod
    def process_entity(cls, entity):
        """Turn json entity into a dictionary"""
        output = entity.copy()
        # Hold relation objects in specific dict. T1Service instantiates the
        # correct classes.
        relations = {}
        # for legacy/compatibility reasons with existing Entity code.
        if 'entity_type' in output:
            output['_type'] = output['entity_type']

        for key, val in six.iteritems(output):
            if type(val) is dict and 'entity_type' in val:  # Get parent entities recursively
                cls.process_related_entity(relations, val, key)
            elif type(val) is list and 'entity_type' in next(iter(val), {}):
                for child in val:
                    cls.process_related_entity(relations, child, key)
            # this is new as we are potentially returning multiple
            # currency types, but for now let's grab the first value
            elif type(val) is list and 'currency_code' in next(iter(val), {}):
                output[key] = val[0]['value']

        if relations:
            output['relations'] = relations
        return output

    @classmethod
    def process_related_entity(cls, relations, val, array_name):
        ent = cls.process_entity(val)
        relation = val.get('rel')
        if not relation:
            relation = array_name
        if relation == ent['_type']:
            relations[relation] = ent
        else:
            relations.setdefault(relation, []).append(ent)

    @staticmethod
    def process_permission(permission, type):
        if not permission:
            return
        output = {}
        permission = permission[0]
        for access in permission['access']:
            if type == 'flags':
                output[access['type']] = access['value']
            else:
                output[int(access['id'])] = JSONParser.dictify_access_flag(access)
        return output

    @staticmethod
    def dictify_access_flag(flag):
        output = flag
        for key in output.keys():
            if 'id' == key or key.endswith('_id'):
                output[key] = int(output[key])
        return output
