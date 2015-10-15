# -*- coding: utf-8 -*-
"""Parses JSON output from T1 and returns a Python object"""

from __future__ import absolute_import
import json

from .errors import (T1Error, APIError, ClientError, ValidationError,
                     AuthRequiredError, NotFoundError)

# Map known status.code repsonses to Exceptions. 'ok' signifies no exception,
# so that is None. 'invalid' can have many errors and needs
# an additional level of parsing, while the others can be instantiated directly.
STATUS_CODES = {
    'ok': None,
    'invalid': True,
    'not_found': NotFoundError,
    'auth_required': AuthRequiredError,
    'auth_error': AuthRequiredError,
    'error': APIError,
    'bad_request': ClientError,
}


class FindKey:
    def __init__(self, data, key):
        self.i = 0
        self.json = data
        self.key = key

    def __iter__(self):
        return self

    def next(self):
        try:
            self.json = self.json[self.key]
            return self.json
        except KeyError:
            raise StopIteration()


class JSONParser(object):
    """Parses JSON response"""

    def __init__(self, body):
        self.status_code = False
        parsed_data = json.loads(body)

        self.get_status(parsed_data, body)

        try:
            self.entity_count = int(parsed_data['meta']['total_count'])
        except KeyError:
            self.entity_count = 1

        data = parsed_data['data']

        if type(data) == list:
            self.entities = map(self.process_entity, data)

        else:
            if data.get('permissions') is not None:
                self.entities = self._parse_permissions(data['permissions'])
            else:
                self.entities = map(self.process_entity, FindKey(parsed_data, 'data'))

    def get_status(self, data, body):
        """Gets the status code of T1 XML.

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

        raise exc(status_code, message)

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

        # There will only be one instance here.
        # But the caller expects an iterator, so make a list of it
        return [flags, ]

    @staticmethod
    def _parse_field_error(data):
        """Iterate over field errors and parse into dicts"""
        errors = {}
        for error in data['errors']:
            errors[error['field']] = {'code': error['field-error'],
                                      'error': error['message']}
        return errors

    def process_entity(self, entity):
        """Turn json entity into a dictionary"""
        output = entity.copy()
        # Hold relation objects in specific dict. T1Service instantiates the
        # correct classes.
        relations = {}
        # for legacy/compatibility reasons with existing Entity code.
        if 'entity_type' in output:
            output['_type'] = output['entity_type']
            del output['entity_type']

        for key, val in output.iteritems():
            # FIXME this will break if we introduce any other arrays
            if type(val) == list:  # Get parent entities recursively
                for child in val:
                    ent = self.process_entity(child)
                    if child['rel'] == ent['_type']:
                        relations[child['rel']] = ent
                    else:
                        relations.setdefault(child['rel'], []).append(ent)

        if relations:
            output['relations'] = relations
        return output

    @staticmethod
    def process_permission(permission, type):
        if not permission:
            return
        output = {}
        print(permission)
        permission = permission[0]
        for access in permission['access']:
            if type == 'flags':
                output[access['type']] = access['value']
            else:
                output[access['id']] = access['name']
        return output
