# -*- coding: utf-8 -*-
"""Provides configuration data"""

from __future__ import absolute_import, division


VALID_ENVS = frozenset(['production', 'sandbox'])

API_BASES = {
    'production': 'api.mediamath.com',
    'qa': 't1qa10.mediamath.com',
    'sandbox': 't1sandbox.mediamath.com',
}

ACCEPT_HEADERS = {
    'json': 'application/vnd.mediamath.v1+json',
    'xml': ['text/xml', 'application/xml']
}

AUTH_BASES = {
    'qa': 'sso.mediamath-dev.auth0.com',
    'sandbox': 'sso.mediamath-dev.auth0.com',
    'production': 'auth.mediamath.com'
}

SERVICE_BASE_PATHS = {
    'deals': 'media/v1.0',
    'mgmt': 'api/v2.0',
    'reports': 'reporting/v1/std',
    'uniques': 'uniques/v1',
    'oauth2': 'oauth2/v1.0',
}
