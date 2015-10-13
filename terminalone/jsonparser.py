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


class FindData:
    def __init__(self, data):
        self.i = 0
        self.json = data

    def __iter__(self):
        return self

    def next(self):
        try:
            self.json = self.json['data']
            return self.json
        except KeyError:
            raise StopIteration()

class JSONParser(object):
    """Parses JSON response"""

    def __init__(self, body):
        parsedData = json.loads(body)

        self.get_status(parsedData, body)

        try:
            self.entity_count = parsedData['meta']['total_count']
        except KeyError:
            self.entity_count = 1

        data = parsedData['data']

        if type(data) == list:
            self.entities = map(self.dictify_entity, data)
        else:
            self.entities = map(self.dictify_entity, FindData(parsedData))

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

        self.status_code = False
        if exc is True:
            message = self._parse_field_error(data)
            exc = ValidationError

        raise exc(status_code, message)

    @staticmethod
    def _parse_field_error(data):
        """Iterate over field errors and parse into dicts"""
        errors = {}
        for error in data['errors']:
            errors[error['field']] = {'code': error['field-error'],
                                       'error': error['message']}
        return errors


    def dictify_entity(self, entity_key):
        """Turn json entity into a dictionary"""
        output = entity_key.copy()
        # Hold relation objects in specific dict. T1Service instantiates the
        # correct classes.
        relations = {}
        #for legacy/compatibility reasons with existing Entity code.
        if 'entity_type' in output:
            output['_type'] = output['entity_type']
            del output['entity_type']

        #for prop in entity:
            #if prop.tag == 'entity':  # Get parent entities recursively
            #    ent = self.dictify_entity(prop)
            #    if prop.attrib['rel'] == ent.get('_type'):
            #        relations[prop.attrib['rel']] = ent
            #    else:
            #        relations.setdefault(prop.attrib['rel'], []).append(ent)
            #else:
            #output[prop.attrib['name']] = prop.attrib['value']
        #if relations:
        #    output['relations'] = relations
        return output
