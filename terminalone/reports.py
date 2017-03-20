# -*- coding: utf-8 -*-
"""Provides reporting data."""

from __future__ import absolute_import, division
import csv
from .config import SERVICE_BASE_PATHS
from .connection import Connection
from .errors import ClientError, T1Error
from .utils import compose
from .vendor import six
from .vendor.six.moves.urllib.parse import unquote, urlencode
from .xmlparser import ParseError, XMLParser

if six.PY3:
    decode = True
else:
    decode = False


class Report(Connection):
    """Object for pulling reports"""
    _fields = {
        'dimensions': ','.join,
        'end_date': None,
        'filter': compose(unquote, urlencode),
        'having': compose(unquote, urlencode),
        'metrics': ','.join,
        'order': ','.join,
        'start_date': None,
        'time_window': None,
        'time_rollup': None,
    }

    def __init__(self, session, report=None, properties=None, **kwargs):
        super(Report, self).__init__(_create_session=False, **kwargs)
        self.session = session
        self.parameters = {}

        if report is not None:
            self.report = report

        if properties is not None:
            self.set(properties)
        elif kwargs:
            self.set(kwargs)

    def __getattr__(self, attr):
        if attr in self.parameters:
            return self.parameters[attr]
        else:
            raise AttributeError(attr)

    def __setattr__(self, key, value):
        if key in self._fields:
            self.parameters[key] = value
        else:
            super(Report, self).__setattr__(key, value)

    def report_uri(self, report):
        """Get report URI stub from metadata info.

        e.g. report_uri('https://api.../reporting/v1/std/performance') ->
             'performance'
        """
        metadata = self.metadata
        if not hasattr(self, 'report'):
            if report not in metadata['reports']:
                raise ClientError('Invalid report')

            return metadata['reports'][report]['URI_Data'].rsplit('/', 1)[-1]
        else:
            return metadata['URI_Data']

    def set(self, data):
        """Set properties for report from given dict of properties.

        Essentially a merge.
        """
        for field, value in six.iteritems(data):
            setattr(self, field, value)

    def _get(self, path, params=None):
        """Base method customized for the mix of JSON and XML

        :param path: str path to hit. Should not start with slash
        :param params: dict query string params
        """
        url = '/'.join(['https:/', self.api_base, SERVICE_BASE_PATHS['reports'], path])
        response = self.session.get(url, params=params, stream=True)

        if not response.ok:
            try:
                result = XMLParser(response.content)
            except ParseError as exc:
                self.response = response
                raise ClientError('Could not parse XML response: {!r}'.format(exc))
            raise T1Error(result, None)

        return response

    @property
    def metadata(self):
        """Fetch report metadata.

        If no report is given, fetches metadata for all reports.
        Caches for future use.
        """
        if hasattr(self, '_metadata'):
            return self._metadata

        if hasattr(self, 'report'):
            path = self.report + '/meta'
        else:
            path = 'meta'

        res = self._get(path)

        self._metadata = res.json()
        return self._metadata

    def get(self, as_dict=False):
        """Get report data. Returns tuple (headers, csv.Reader).

        If as_dict == True, return (headers, csv.DictReader).
        """
        if not hasattr(self, 'report'):
            raise ClientError("Can't run get without report!")

        params = {}
        for key, value in six.iteritems(self.parameters):
            if self._fields[key]:
                params[key] = self._fields[key](value)
            else:
                params[key] = value

        iter_ = self._get(self.report,
                          params=params).iter_lines(decode_unicode=decode)

        if as_dict:
            reader = csv.DictReader(iter_)
            headers = reader.fieldnames
        else:
            reader = csv.reader(iter_)
            headers = next(reader)

        return headers, reader
